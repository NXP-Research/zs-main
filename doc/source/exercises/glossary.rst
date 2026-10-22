.. _workshop-glossary:

Glossary
========

The words you meet in the workshop, in alphabetical order. The exercise
number shows where the word appears first. For more terms, see the official
:zdoc:`Zephyr glossary <glossary>`.

.. glossary::
   :sorted:

   Alias
      A standard name for a board part in the :term:`Devicetree`, for example
      ``led0`` or ``sw0``. Code that uses aliases runs on every board that
      defines them. (Exercise 2)

   Active low
      The part is *on* when the pin is at 0 V. The LEDs and buttons of the
      FRDM-MCXA156 are active low. Zephyr handles the inversion: in your code,
      ``1`` always means "active". (Exercise 2)

   Atomic variable
      A variable of type ``atomic_t``, read and changed only with the
      ``atomic_*()`` functions. Each access is one step that an interrupt
      cannot cut in half, so an :term:`ISR` and a :term:`thread` can share
      it safely. (Exercise 4)

   Blocking call
      A call that can make the calling :term:`thread` wait, for example
      ``k_msleep()`` or ``k_msgq_get()`` with ``K_FOREVER``. Not allowed in
      an :term:`ISR`. (Exercise 4)

   Board
      The printed circuit board with the chip, LEDs, buttons and connectors,
      here the FRDM-MCXA156. You select it with ``-b`` in ``west build``.
      (Exercise 1)

   Callback
      A function that you give to a driver, and that the driver calls later,
      when something happens. ``button_pressed()`` is a callback. (Exercise 3)

   Contact bounce
      A mechanical button does not close cleanly: the contacts open and close
      several times within a few milliseconds, on press and on release. The
      code sees several edges for one press. Filtering them is called
      *debouncing*. (Exercise 3)

   Devicetree
      Text files that describe the hardware: which LEDs, buttons and
      controllers exist and to which pins they are connected. At build time it
      becomes C macros. (Exercise 2)

   Edge
      The moment a pin changes level: from inactive to active, or back. GPIO
      interrupts can fire on edges. (Exercise 3)

   Flash
      1. The non-volatile memory of the chip, where the program is stored.
      2. Writing the program into it, with ``west flash``. (Exercise 1)

   GPIO
      General Purpose Input/Output: a pin that the software can set (output,
      for an LED) or read (input, for a button). (Exercise 2)

   Interrupt
      A signal from the hardware that stops the normal program for a moment
      and runs an :term:`ISR`. (Exercise 3)

   ISR
      Interrupt Service Routine: the code that runs when an
      :term:`interrupt` fires. It must be short and must never wait.
      (Exercise 3)

   Kconfig
      Zephyr's configuration system. ``CONFIG_...`` options in ``prj.conf``
      select which features and drivers are built into the program.
      (Exercise 1)

   Kernel
      The core of Zephyr: it runs the :term:`threads <thread>`, and provides
      timing, queues and other services. (Exercise 1)

   LinkServer
      NXP's tool that talks to the debug probe on the board. ``west flash``
      uses it to write the program. (Exercise 1)

   MCU-Link
      The debug probe built into the board, behind the USB port J21. It flashes
      the chip and forwards its :term:`serial console` to the PC.
      (Exercise 1)

   Message queue
      A ``k_msgq``: a queue of fixed-size messages, first in, first out. One
      side puts messages in, the other side takes them out. Safe to use
      between an :term:`ISR` and a :term:`thread`. (Exercise 4)

   Overlay
      A Devicetree file in your application folder that changes the board's
      :term:`Devicetree` without touching the board files. (Exercise 2)

   Polling
      Checking a value again and again in a loop, instead of waiting for an
      :term:`interrupt`. (Exercise 3)

   Preemptible
      A :term:`thread` with a priority ``>= 0``. The scheduler can stop it at
      any time to run a thread with a higher priority. (Exercise 4)

   Priority
      A number that tells the scheduler which :term:`thread` to run first.
      Lower number = higher priority. (Exercise 4)

   Pristine build
      A clean build that first deletes the old build folder: ``west build -p``.
      (Exercise 1)

   Scheduler
      The part of the :term:`kernel` that decides which :term:`thread` runs.
      It always runs the ready thread with the highest :term:`priority`.
      (Exercise 4)

   Serial console
      The text output of the board, sent over a UART to the PC. You read it
      with minicom (Linux) or PuTTY (Windows) at 115200 baud. (Exercise 1)

   SoC
      System on Chip: the microcontroller itself, here the MCXA156. The
      ``/mcxa156`` in ``frdm_mcxa156/mcxa156`` is the SoC. (Exercise 1)

   Stack
      The memory a :term:`thread` uses for its local variables and function
      calls. Each thread has its own. (Exercise 4)

   State machine
      A program design where the program is always in one of a few named
      states, and events move it from one state to the next. (Exercise 5)

   Thread
      An independent flow of execution with its own :term:`stack` and
      :term:`priority`. ``main()`` runs in a thread too. (Exercise 1)

   Timeout
      The longest time a :term:`blocking call` may wait: ``K_NO_WAIT``
      (never wait), ``K_MSEC(100)`` or ``K_FOREVER``. (Exercise 4)

   west
      Zephyr's command line tool. It builds (``west build``), flashes
      (``west flash``) and manages the source repositories. (Exercise 1)
