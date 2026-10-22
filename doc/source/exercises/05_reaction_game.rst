.. _exercise-reaction-game:

Exercise 5: Reaction Game
=========================

**Goal:** put everything together into a small game.

1. Press **SW2** to start a round.
2. After a **random** delay of 1 to 4 seconds, the red LED turns on.
3. Press SW2 as fast as you can. The reaction time is printed.

.. code-block:: none

   === Reaction Game ===

   Press SW2 to start round 1
   Get ready... press when the LED turns on!
     Reaction time: 243.118 ms
     New best!
     Rounds: 1, best: 243 ms, average: 243 ms

   Press SW2 to start round 2
   Get ready... press when the LED turns on!
     Too early! Wait for the LED.

**Concepts:** GPIO, interrupts, synchronization, timing, application state
management (state machines).

**Sample:** ``zephyr/samples/workshop/reaction_game`` (solution in
``zephyr/samples/workshop/reaction_game/solution``)

Design
------

The game reuses the ISR → message queue → thread pattern from exercise 4. This
time the thread that receives the button events is the ``main()`` thread,
which runs the game as a **state machine**:

.. image:: ../_static/images/exercises_reaction_states.svg
   :align: center
   :alt: State machine: IDLE goes to WAITING on a press. WAITING goes back to IDLE on a press (too early) or to REACT when the delay expires. REACT goes back to IDLE on a press or on timeout.

The same transitions as a table:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - From
     - Event
     - To
     - Action

   * - ``STATE_IDLE``
     - press
     - ``STATE_WAITING``
     - LED off, pick a random delay

   * - ``STATE_WAITING``
     - press
     - ``STATE_IDLE``
     - "Too early!"

   * - ``STATE_WAITING``
     - delay expired
     - ``STATE_REACT``
     - LED on, remember the time

   * - ``STATE_REACT``
     - press
     - ``STATE_IDLE``
     - LED off, print the reaction time

   * - ``STATE_REACT``
     - ``REACT_TIMEOUT_MS`` expired
     - ``STATE_IDLE``
     - LED off, "Too slow!"

Things to notice:

- **Application state** lives in one variable, ``state``, owned by a single
  thread. Only the message queue is shared with the ISR, so there are no race
  conditions on the game data.
- **A timeout is an event too.** ``k_msgq_get(..., K_MSEC(delay))`` means
  "wait for a press, but at most ``delay`` ms". The return value tells you
  which one happened: ``0`` means a press arrived, ``-EAGAIN`` means the time
  ran out. One call implements both the random delay *and* the false-start
  detection.
- **Accurate timing.** The ISR stores ``k_cycle_get_32()``, the hardware cycle
  counter, at the moment of the press. The game thread may run a little later,
  but the timestamp is exact. ``k_cyc_to_us_floor32()`` converts cycles to
  microseconds.
- **Debouncing in the ISR.** This time we drop bounces directly in the ISR,
  with a single subtraction. That is cheap enough for an ISR and keeps the
  game logic simple.
- **Random numbers.** The board configuration has no hardware entropy driver
  enabled, so the starter provides a tiny pseudo-random generator,
  ``rng_next()``. Seed it with ``rng_mix()`` using the timestamps of the
  player's button presses, which are unpredictable enough for a game.

Your tasks
----------

Open ``zephyr/samples/workshop/reaction_game/src/main.c``. It contains the
timing constants, the ``enum game_state`` and the random number helpers.
Start by copying the message queue, the ISR and the GPIO setup from
exercise 4. You don't need the threads from exercise 4 this time.

1. **ISR.** Store ``k_cycle_get_32()`` in the event instead of milliseconds.
   Drop presses that come less than ``DEBOUNCE_MS`` after the previous
   accepted one (``k_cyc_to_ms_floor32()`` converts cycles to ms).
2. **Game loop.** In ``main()``, write a ``while (1)`` loop with a ``switch``
   on ``state``. In ``STATE_IDLE``, wait for a press with ``K_FOREVER``, seed
   the random generator and go to ``STATE_WAITING``.
3. **Random delay.** In ``STATE_WAITING``, pick a delay between
   ``MIN_DELAY_MS`` and ``MAX_DELAY_MS``. Hint: ``rng_next() % N`` gives a
   number from 0 to N - 1.
4. **False starts.** Wait for a press with the delay as timeout. If a press
   arrives, print "Too early!" and go back to ``STATE_IDLE``. Otherwise turn
   the LED on, save ``k_cycle_get_32()`` and go to ``STATE_REACT``.
5. **Measure.** In ``STATE_REACT``, wait for a press with
   ``REACT_TIMEOUT_MS`` as timeout. Turn the LED off. On a press, compute and
   print the reaction time in microseconds from the two cycle counter values.
   On a timeout, print "Too slow!". Then go back to ``STATE_IDLE``.
6. Bonus: keep statistics: number of rounds, best and average reaction time.

Build and flash after each step:

.. code-block:: bash

   west build -p -b frdm_mcxa156/mcxa156 zephyr/samples/workshop/reaction_game
   west flash

.. note::

   Unsigned subtraction handles counter wrap-around: ``end - start`` is
   correct even if the 32-bit cycle counter overflowed in between, as long as
   less than one full counter period has passed.

Ideas for extensions
--------------------

- **Best of 5:** play five rounds, then print a summary and reset the
  statistics.
- **Two players:** SW2 (``sw0``) against SW3 (``sw1``). Who presses first
  after the LED turns on? Use one message queue and put the button ID in the
  event.
- **Color feedback:** after a round, light the green LED (``led1``) for a good
  time (below 250 ms) and the blue LED (``led2``) otherwise.
- **Separate thread:** move the game into its own thread with
  ``K_THREAD_DEFINE`` and keep the heartbeat from exercise 4 running.
- **Shell:** enable ``CONFIG_SHELL=y`` and add a ``game stats`` command. See
  ``zephyr/samples/subsys/shell/shell_module`` for an example.

Discussion
----------

- Why is the timestamp captured in the ISR and not in the thread?
- Which variables are accessed from both the ISR and a thread? Why is that
  safe here?
- What happens to button presses that arrive while the game is printing?
