.. _exercise-hello-world:

Exercise 1: Hello Zephyr
========================

**Goal:** build your first Zephyr application, flash it to the FRDM-MCXA156 and
see its output on the serial console.

**Concepts:** Zephyr application structure, ``west``, board selection, the
build/flash process, the serial console.

**Sample:** ``zephyr/samples/hello_world``

Anatomy of a Zephyr application
-------------------------------

A Zephyr application is a directory with at least three files:

.. code-block:: none

   zephyr/samples/hello_world/
   ├── CMakeLists.txt   <- tells CMake "this is a Zephyr app" and lists the sources
   ├── prj.conf         <- Kconfig options: which kernel features and drivers to enable
   └── src/
       └── main.c       <- your code: Zephyr calls main() after booting

Open each file and read it.

- ``find_package(Zephyr ...)`` in ``CMakeLists.txt`` pulls in the whole Zephyr
  build system. ``target_sources(app ...)`` adds your source files to the
  application.
- ``prj.conf`` is empty. That is fine: the board already ships sensible
  defaults in ``zephyr/boards/nxp/frdm_mcxa156/frdm_mcxa156_defconfig``, for
  example the serial console.
- ``main()`` runs in a normal **thread**, the *main thread*. When ``main()``
  returns, only the main thread ends. The kernel keeps running.

Build it
--------

This is the path from your source code to text on your screen:

.. image:: ../_static/images/exercises_build_flow.svg
   :align: center
   :alt: west build turns your application plus Zephyr into zephyr.elf, west flash writes it to the board, and the board prints to the serial terminal over UART.

From ``zephyr-workdir``:

.. code-block:: bash

   west build -p -b frdm_mcxa156/mcxa156 zephyr/samples/hello_world

- ``-b frdm_mcxa156/mcxa156`` selects the **board** (and its SoC). Zephyr
  supports hundreds of boards, and the same source code builds for all of
  them. Try ``west boards -n mcx`` to list the boards whose name contains
  ``mcx``.
- ``-p`` makes a **pristine** (clean) build.
- The output goes to the ``build/`` directory. The final image is
  ``build/zephyr/zephyr.elf`` (plus ``zephyr.hex`` and ``zephyr.bin``).

At the end of the build you get a memory usage report:

.. code-block:: none

   Memory region         Used Size  Region Size  %age Used
              FLASH:       17756 B         1 MB      1.69%
                RAM:        4032 B       120 KB      3.28%

Remember these numbers and compare them with the next exercises.

You will also see a few warnings during the build, for example:

.. code-block:: none

   warning: LPADC_DO_OFFSET_CALIBRATION (...) was assigned the value 'y' but got the value 'n'.
   Check these unsatisfied dependencies: ADC_MCUX_LPADC (=n), ADC (=n).

They are harmless. This one is a good first example of how Kconfig works:
the board's default configuration sets an ADC option, but the ADC driver is not
enabled in this application. Options have **dependencies**, and an option
whose dependencies are not met cannot be enabled.

Flash it and open the console
-----------------------------

Follow :doc:`../flashing_the_board` to open the serial console, then flash:

.. code-block:: bash

   west flash

``west flash`` uses the last build and calls the board's default *runner*,
LinkServer for this board.

You should see the Zephyr boot banner, followed by the output of ``main()``:

.. code-block:: none

   *** Booting Zephyr OS build v4.4.2 ***
   Hello World! frdm_mcxa156/mcxa156

If you missed it, press the **RESET** button on the board.

Your tasks
----------

Now change the application. Edit
``zephyr/samples/hello_world/src/main.c``:

1. Print ``Hello Zephyr!`` and the name of the board. The board name is
   available as the Kconfig symbol ``CONFIG_BOARD_TARGET`` (a string).

2. Print a "heartbeat" message once per second, forever, with a counter and
   the system uptime in milliseconds:

   .. code-block:: none

      Hello Zephyr! Running on frdm_mcxa156/mcxa156
      [     1001 ms] tick 1
      [     2002 ms] tick 2
      [     3003 ms] tick 3

   Hints:

   - Include ``<zephyr/kernel.h>`` to use the kernel APIs.
   - ``k_msleep(ms)`` puts the current thread to sleep for ``ms`` milliseconds.
   - ``k_uptime_get()`` returns the uptime in milliseconds as an ``int64_t``.
     Print it with ``%lld``.
   - ``printk()`` is Zephyr's own lightweight ``printf()``. Both work here.

3. Rebuild and flash. You don't need ``-p`` now: ``west build`` without
   arguments does an incremental build of the same application.

   .. code-block:: bash

      west build
      west flash

Going further
-------------

- Open ``build/zephyr/.config``. This is the *final* configuration: every
  Kconfig option with its value. Search for ``CONFIG_PRINTK`` and
  ``CONFIG_SERIAL``.
- Add ``CONFIG_BOOT_BANNER=n`` to ``prj.conf``, rebuild and flash. The banner
  is gone. Did the FLASH usage change?
- Run ``west build -t menuconfig`` to browse all options interactively.
- Run ``west build -t rom_report`` to see what takes up flash.

Discussion
----------

- What does ``west`` do, and what does CMake do? (``west`` is a meta-tool: it
  manages the workspace repositories and wraps CMake, Ninja and the flash and
  debug tools.)
- Why does the same ``main.c`` build for many different boards?
- What does the CPU do while your thread sleeps in ``k_msleep()``?

Solution
--------

.. code-block:: c

   #include <zephyr/kernel.h>
   #include <zephyr/sys/printk.h>

   int main(void)
   {
           uint32_t tick = 0;

           printk("Hello Zephyr! Running on %s\n", CONFIG_BOARD_TARGET);

           while (1) {
                   /* Sleeping lets the CPU run other threads (or idle). */
                   k_msleep(1000);
                   tick++;

                   printk("[%9lld ms] tick %u\n", k_uptime_get(), tick);
           }

           return 0;
   }
