.. _exercise-threads:

Exercise 4: Threads
===================

**Goal:** start thinking like an RTOS developer. Move the application logic out
of the interrupt and into a thread:

.. image:: ../_static/images/exercises_threads_msgq.svg
   :align: center
   :alt: The ISR puts a button event into the message queue without waiting. The worker thread sleeps until it gets the event and toggles the red LED. A separate heartbeat thread blinks the green LED.

**Concepts:** threads, priorities, message queues, blocking vs. non-blocking
calls, ISR vs. thread context.

**Sample:** ``zephyr/samples/workshop/threads`` (solution in
``zephyr/samples/workshop/threads/solution``)

Why not do everything in the ISR?
---------------------------------

In exercise 3 the ISR toggled the LED and called ``printk()``. That works for a
tiny demo, but real work, like talking to a sensor, updating a display or
sending data, is too slow for an ISR. It often needs APIs that **block**,
which is not allowed in an ISR. The usual pattern is:

- the **ISR** records *what* happened (and *when*) and hands it over, without
  waiting;
- a **thread** waits for these events and does the actual work.

Threads
-------

A thread is an independent flow of execution with its own stack and a
**priority**. The scheduler always runs the highest-priority thread that is
*ready*. A thread that waits (because it sleeps or waits on a queue) is not
ready and uses no CPU time.

The easiest way to create a thread is to define it statically. It starts
automatically after boot:

.. code-block:: c

   static void worker_thread(void *p1, void *p2, void *p3)
   {
           while (1) {
                   /* wait for work, then do it */
           }
   }

   K_THREAD_DEFINE(worker_tid, 1024, worker_thread, NULL, NULL, NULL,
                   5 /* priority */, 0 /* options */, 0 /* start delay */);

- **Lower number = higher priority.**
- Priorities ``>= 0`` are *preemptible*: when a higher-priority thread becomes
  ready, it interrupts them immediately. Negative priorities are
  *cooperative*: they run until they give up the CPU themselves.
- ``main()`` itself runs in a thread, with priority 0 by default.

In this exercise you write two threads: ``worker`` (priority 5) handles the
button, and ``heartbeat`` (priority 7) blinks the green LED on its own.

Message queues
--------------

A ``k_msgq`` is a thread-safe FIFO of fixed-size messages, copied by value:

.. code-block:: c

   struct button_event {
           uint32_t timestamp_ms;
   };

   /* name, size of one message, max number of messages, alignment */
   K_MSGQ_DEFINE(button_msgq, sizeof(struct button_event), 8, 4);

   k_msgq_put(&button_msgq, &evt, K_NO_WAIT);  /* producer (ISR) */
   k_msgq_get(&button_msgq, &evt, K_FOREVER);  /* consumer (thread) */

The last argument is the **timeout**. It decides whether the call blocks:

.. list-table::
   :header-rows: 1
   :widths: 20 55 25

   * - Timeout
     - Behavior
     - Allowed in an ISR?

   * - ``K_NO_WAIT``
     - Return immediately, with an error if not possible
     - yes

   * - ``K_MSEC(100)``
     - Wait at most 100 ms, then return ``-EAGAIN``
     - no

   * - ``K_FOREVER``
     - Wait as long as it takes
     - no

Your tasks
----------

Open ``zephyr/samples/workshop/threads/src/main.c``. It contains the thread
priorities, the stack size and hints. Start by copying your code from
exercise 3: the ``gpio_dt_spec`` variables, the callback and the setup in
``main()``.

1. Define ``struct button_event`` and the message queue ``button_msgq``.
2. Change the ISR: instead of toggling the LED, fill a ``struct button_event``
   with ``k_uptime_get_32()`` and put it into the queue with ``K_NO_WAIT``.
3. Write ``worker_thread()``: in a loop, wait for an event with
   ``K_FOREVER``, toggle the red LED and print the event timestamp.
4. Write ``heartbeat_thread()``: configure the green LED (``led1``) and
   toggle it once per second.
5. Define both threads with ``K_THREAD_DEFINE``, using ``WORKER_PRIORITY``,
   ``HEARTBEAT_PRIORITY`` and ``STACK_SIZE``.
6. Bonus: **debounce**. In the worker, ignore events that arrive less than
   ``DEBOUNCE_MS`` after the last accepted one. This is easy now, because the
   timestamp is in the message.

Build and flash:

.. code-block:: bash

   west build -p -b frdm_mcxa156/mcxa156 zephyr/samples/workshop/threads
   west flash

The red LED toggles on each press, while the green LED blinks on its own. Both
are in the same RGB LED, so you will see the colors mix.

.. code-block:: none

   Press SW2: the worker thread toggles the red LED
   [  3120 ms] press 1
   [  4518 ms] press 2

Going further
-------------

- **Context check:** print ``k_is_in_isr()`` in the worker. Compare with
  exercise 3.
- **Timeouts:** replace ``K_FOREVER`` in the worker with ``K_SECONDS(5)`` and
  print ``No button press for 5 s`` when ``k_msgq_get()`` returns
  ``-EAGAIN``.
- **Queue overflow:** reduce the queue to 1 entry and add ``k_msleep(2000)``
  to the worker after each event, to simulate slow work. Press the button
  quickly several times. What happens to the extra presses? Count the failed
  ``k_msgq_put()`` calls in the ISR and print the count. The solution does
  this.
- **Priorities and starvation:** in the worker, after toggling the LED, add
  ``k_busy_wait(3000000);`` (3 s of busy-waiting: the CPU spins without
  sleeping). Press the button: the heartbeat LED **stops** for 3 s, because
  the higher-priority worker never gives up the CPU. Now swap the priorities
  (worker 7, heartbeat 5) and try again. Then replace ``k_busy_wait()`` with
  ``k_msleep()`` and explain the difference.
- **Stack usage:** add ``CONFIG_THREAD_NAME=y``, ``CONFIG_THREAD_ANALYZER=y``
  and ``CONFIG_THREAD_ANALYZER_AUTO=y`` to ``prj.conf`` to periodically print
  the stack usage of each thread.

Discussion
----------

- What is the difference between ``k_msleep(3000)`` and
  ``k_busy_wait(3000000)`` for the *other* threads?
- Why must the ISR use ``K_NO_WAIT``?
- Why do we put the timestamp into the message instead of reading the time in
  the worker?
