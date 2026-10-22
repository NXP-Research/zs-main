.. _exercise-blinky:

Exercise 2: Blinky
==================

**Goal:** blink the red LED on the board.

**Concepts:** GPIO, basic Devicetree (``led0``, ``gpio_dt_spec``), Kconfig and
``prj.conf``, the Zephyr device model.

**Sample:** ``zephyr/samples/basic/blinky``

Build and flash it first
------------------------

.. code-block:: bash

   west build -p -b frdm_mcxa156/mcxa156 zephyr/samples/basic/blinky
   west flash

The red LED blinks once per second and the console prints:

.. code-block:: none

   LED state: OFF
   LED state: ON
   LED state: OFF

Now open ``zephyr/samples/basic/blinky/src/main.c`` and follow along.

Where does "the LED" come from? Devicetree
------------------------------------------

The C code does not say "port 3, pin 12". Instead, the hardware is described
in **Devicetree** files, and the code refers to it by name. Open
``zephyr/boards/nxp/frdm_mcxa156/frdm_mcxa156.dts`` and find:

.. code-block:: dts

   aliases {
           led0 = &red_led;
           led1 = &green_led;
           led2 = &blue_led;
           sw0 = &user_button_2;
           ...
   };

   leds {
           compatible = "gpio-leds";

           red_led: led_0 {
                   gpios = <&gpio3 12 GPIO_ACTIVE_LOW>;
                   label = "Red LED";
           };
           ...
   };

- ``led0`` is an **alias**, a standard name that many Zephyr samples use. On
  another board, ``led0`` points to a different pin, and the same code still
  works.
- ``gpios = <&gpio3 12 GPIO_ACTIVE_LOW>`` means: GPIO controller ``gpio3``,
  pin 12, and the LED is *on* when the pin is *low*. Zephyr handles the
  inversion for you: "1" always means "active" (LED on).

At build time, the Devicetree is turned into C macros. The sample uses them
like this:

.. code-block:: c

   #define LED0_NODE DT_ALIAS(led0)

   static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

A ``struct gpio_dt_spec`` bundles everything the GPIO API needs: the GPIO
controller **device** (``led.port``), the pin number (``led.pin``) and the
flags (``led.dt_flags``, for example active low).

The device model
----------------

In Zephyr, every driver instance is a ``const struct device``. Drivers are
initialized automatically at boot, before ``main()`` runs. Before you use a
device, check that its initialization succeeded:

.. code-block:: c

   if (!gpio_is_ready_dt(&led)) {
           return 0;
   }

Then the sample configures the pin as an output and toggles it in a loop:

.. code-block:: c

   ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
   ...
   while (1) {
           ret = gpio_pin_toggle_dt(&led);
           ...
           k_msleep(SLEEP_TIME_MS);
   }

All functions ending in ``_dt`` take a ``gpio_dt_spec``. Most of them return
``0`` on success and a negative error code on failure.

Putting it together: the Devicetree decides *which* pin, the build turns it
into a ``gpio_dt_spec``, and at run time the GPIO driver drives the pin:

.. image:: ../_static/images/exercises_blinky_devicetree.svg
   :align: center
   :alt: At build time the led0 alias in the board Devicetree becomes a gpio_dt_spec in C. At run time main() calls gpio_pin_toggle_dt, the GPIO driver drives pin P3_12 and the LED turns on or off.

Kconfig: enabling the GPIO driver
---------------------------------

Drivers are only compiled in if they are enabled in Kconfig. The sample's
``prj.conf`` contains one line:

.. code-block:: none

   CONFIG_GPIO=y

This enables the GPIO subsystem. On this board it happens to be enabled by
default already, but it is good practice to state what your application needs
in ``prj.conf``.

Your tasks
----------

Edit the sample and rebuild with ``west build`` after each change:

1. Change the blink period to 200 ms.
2. Print an error message (with ``printf()``) when ``gpio_is_ready_dt()`` or
   ``gpio_pin_configure_dt()`` fails, instead of returning silently. Print the
   error code too.
3. Blink the green LED (``led1``) instead of the red one.
4. Blink red and green alternately: one is on while the other is off. You need
   a second ``gpio_dt_spec``.

Going further
-------------

- Open ``build/zephyr/zephyr.dts``, the final, merged Devicetree, and search
  for ``led_0``. Then open
  ``build/zephyr/include/generated/zephyr/devicetree_generated.h`` to see the
  macros generated from it.
- **Devicetree overlay:** you can change the hardware description without
  touching the board files. Create ``boards/frdm_mcxa156.overlay`` in the
  application directory with:

  .. code-block:: dts

     / {
             aliases {
                     led0 = &blue_led;
             };
     };

  Undo your change from task 3, then rebuild with ``-p``. The blue LED now
  blinks, and the C code still says ``led0``.
- Compare the FLASH and RAM usage with exercise 1. What added the extra code?

Discussion
----------

- Why use ``led0`` instead of ``gpio3`` pin 12 directly?
- Why does ``gpio_pin_set_dt(&led, 1)`` turn on an LED that is wired active
  low?
- Why does ``main()`` check ``gpio_is_ready_dt()`` before using the LED?
