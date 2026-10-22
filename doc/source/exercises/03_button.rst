.. _exercise-button:

Exercise 3: Button + LED
========================

**Goal:** toggle the red LED each time you press button **SW2**, using an
interrupt instead of polling.

**Concepts:** GPIO input, interrupts, callbacks, ``sw0``/``led0``, ISR context.

**Sample:** ``zephyr/samples/workshop/button`` (solution in
``zephyr/samples/workshop/button/solution``)

Polling vs. interrupts
----------------------

You could read the button in a loop with ``gpio_pin_get_dt()``, but then the
CPU is busy checking it all the time, and you may miss short presses while you
sleep. Instead, we let the GPIO hardware raise an **interrupt** when the pin
changes, and Zephyr calls our **callback** function.

.. image:: ../_static/images/exercises_button_isr.svg
   :align: center
   :alt: Pressing SW2 makes the GPIO hardware raise an interrupt. Zephyr calls the button_pressed callback in ISR context, which toggles the red LED. main() only sets this up once and returns.

The button in Devicetree
------------------------

.. code-block:: dts

   aliases {
           sw0 = &user_button_2;
   };

   gpio_keys {
           compatible = "gpio-keys";

           user_button_2: button_2 {
                   label = "User SW2";
                   gpios = <&gpio1 7 GPIO_ACTIVE_LOW>;
           };
   };

The button is *active low*: pressing it pulls the pin to ground. Like for the
LED, Zephyr hides the inversion, so "active" means "pressed". You get its
``gpio_dt_spec`` the same way as in blinky:

.. code-block:: c

   static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);

Interrupt setup, step by step
-----------------------------

.. code-block:: c

   /* 1. Configure the pin as an input */
   gpio_pin_configure_dt(&button, GPIO_INPUT);

   /* 2. Choose which event triggers the interrupt */
   gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);

   /* 3. Prepare a callback structure (function + pin mask) ... */
   gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));

   /* 4. ... and register it with the GPIO controller */
   gpio_add_callback_dt(&button, &button_cb_data);

``GPIO_INT_EDGE_TO_ACTIVE`` fires when the pin goes from inactive to active,
which means when the button is pressed. Other options are
``GPIO_INT_EDGE_TO_INACTIVE`` (release), ``GPIO_INT_EDGE_BOTH`` and
``GPIO_INT_LEVEL_ACTIVE``.

``button_cb_data`` is a ``static struct gpio_callback``. The GPIO driver keeps
a pointer to it, so it must stay in memory: never put it on the stack of a
function that returns.

The callback function must have this signature:

.. code-block:: c

   static void button_pressed(const struct device *dev, struct gpio_callback *cb,
                              uint32_t pins)

``pins`` is a bit mask of the pins that triggered the interrupt.

Your tasks
----------

Open ``zephyr/samples/workshop/button/src/main.c``. It builds, but it only
prints a message. The comments guide you step by step. Use the blinky sample
as a reference for the LED part.

1. Get a ``gpio_dt_spec`` for ``led0`` and ``sw0``, and declare a
   ``static struct gpio_callback``.
2. Write the callback ``button_pressed()``: toggle the LED and print a press
   counter. Hint: a ``static`` variable keeps its value between calls.
3. In ``main()``: check that both devices are ready.
4. Configure the LED as an output (``GPIO_OUTPUT_INACTIVE``) and the button
   as an input (``GPIO_INPUT``).
5. Configure the button interrupt to fire when the button is pressed.
6. Bind the callback to the button pin and register it.

Check the return value of each call and print an error message if it fails.

Build and flash:

.. code-block:: bash

   west build -p -b frdm_mcxa156/mcxa156 zephyr/samples/workshop/button
   west flash

Each press of SW2 toggles the red LED:

.. code-block:: none

   Press SW2 to toggle the LED
   Button pressed 1 times
   Button pressed 2 times

ISR context: what you must know
-------------------------------

Your callback runs **in interrupt context**, inside the ISR (interrupt service
routine), not in a thread. Add this to the callback and see:

.. code-block:: c

   printk("in ISR: %s\n", k_is_in_isr() ? "yes" : "no");

Rules of thumb for code in an ISR:

- **Keep it short.** While it runs, no thread can run, and interrupts with the
  same or lower priority must wait.
- **Never block.** No ``k_msleep()``, no waiting on a semaphore or queue with
  a timeout, no mutexes. There is no thread to put to sleep.
- Only call APIs documented as *ISR-safe* ("isr-ok" in the API
  documentation), for example ``k_sem_give()``,
  ``k_msgq_put(..., K_NO_WAIT)`` or ``gpio_pin_toggle_dt()``.
- ``printk()`` works, but it is slow: it writes to the UART character by
  character. That is fine for learning, but not for real products.

Try breaking the second rule: add ``CONFIG_ASSERT=y`` to ``prj.conf`` and
``k_msleep(100)`` to the callback. What does the kernel print when you press
the button? Remove both again afterwards.

Going further
-------------

- Press the button many times. Does the counter sometimes jump by 2 or 3 on a
  single press? That is **contact bounce**: the mechanical contacts open and
  close several times within a few milliseconds. You will fix it in
  exercise 4.
- Change the trigger to ``GPIO_INT_EDGE_BOTH`` and keep the LED on only while
  the button is held. Use ``gpio_pin_get_dt(&button)`` and
  ``gpio_pin_set_dt()``.
- Add the second button (``sw1``, SW3) to control the green LED (``led1``).

Discussion
----------

- Why should an ISR be short? What would happen if it took 100 ms?
- ``main()`` returns, but the button still works. Why?
