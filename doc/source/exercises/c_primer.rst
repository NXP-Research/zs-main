.. _c-primer:

The C you need
==============

The exercises are written in C. You don't need to be a C expert, but you will
meet the constructs on this page in every exercise. Read it once before you
start, and come back to it when a line of code looks strange.

Each section shows a short example and then explains it.

Comments
--------

.. code-block:: c

   /* A comment can span
    * several lines. */
   int x = 1; // or run to the end of the line

The compiler ignores comments. The starter files use them to tell you what to
write, in comments named ``Step 1``, ``Step 2``, ...

Variables and types
-------------------

.. code-block:: c

   int ret = 0;
   uint32_t press_count = 0;
   bool pressed = true;

A variable has a **type**, a **name** and usually a start value. The types you
meet most:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Type
     - Meaning

   * - ``int``
     - A whole number that can be negative. Zephyr functions return an
       ``int``: ``0`` for success, a negative number for an error.

   * - ``uint32_t``
     - An unsigned (never negative) 32-bit whole number, from 0 to
       4294967295. Used for counters and times.

   * - ``uint64_t``
     - The same with 64 bits, for very large sums.

   * - ``bool``
     - ``true`` or ``false``.

   * - ``const``
     - Not a type, but a promise: this value never changes.

Every statement ends with a semicolon ``;``. A missing ``;`` is the most
common build error.

``#define`` and ``#include``
----------------------------

.. code-block:: c

   #include <zephyr/kernel.h>

   #define SLEEP_TIME_MS 1000

- ``#include`` pulls in the declarations of a library, so that you can call
  its functions. ``zephyr/kernel.h`` gives you threads, timing and message
  queues. ``zephyr/drivers/gpio.h`` gives you the GPIO API.
- ``#define`` gives a name to a value. Before compiling, every
  ``SLEEP_TIME_MS`` in the file is replaced by ``1000``. By convention these
  names are in ``UPPER_CASE``.

Names in ``UPPER_CASE`` with parentheses, like ``GPIO_DT_SPEC_GET(...)`` or
``K_MSGQ_DEFINE(...)``, are **macros**: they also get replaced by code before
compiling. You use them like functions.

Functions
---------

.. code-block:: c

   static void button_pressed(const struct device *dev, struct gpio_callback *cb,
                              uint32_t pins)
   {
           /* body */
   }

From left to right: ``static`` (only visible in this file), the **return
type** (``void`` means: returns nothing), the **name**, and the
**parameters** in parentheses, each with its type. The body is between
``{`` and ``}``.

``ARG_UNUSED(dev);`` tells the compiler "I know I don't use this parameter",
so that it does not warn about it.

A function must be defined (or declared) **above** the place where it is used.

``if``, ``while`` and ``continue``
----------------------------------

.. code-block:: c

   if (ret < 0) {
           printk("Error %d\n", ret);
           return 0;
   }

   while (1) {
           k_msgq_get(&button_msgq, &evt, K_FOREVER);
           if (!evt.pressed) {
                   continue;
           }
           press_count++;
   }

- ``if (condition) { ... }`` runs the block only if the condition is true.
- ``while (1) { ... }`` repeats the block forever. Embedded programs often
  have such a loop: there is no "end" of the program.
- ``continue`` jumps back to the start of the loop, skipping the rest.
- ``return`` leaves the function.

Operators you will see:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Operator
     - Meaning

   * - ``==`` ``!=`` ``<`` ``>=``
     - Equal, not equal, less than, greater or equal. Note: ``=`` assigns a
       value, ``==`` compares.

   * - ``!`` ``&&`` ``||``
     - Not, and, or.

   * - ``x++``
     - Add 1 to ``x``.

   * - ``+=``
     - ``total += x`` is short for ``total = total + x``.

   * - ``/`` ``%``
     - Division and remainder of whole numbers: ``1234 / 1000`` is ``1``,
       ``1234 % 1000`` is ``234``.

   * - ``cond ? a : b``
     - ``a`` if ``cond`` is true, else ``b``.

``switch`` and ``case``
-----------------------

.. code-block:: c

   switch (state) {
   case STATE_IDLE:
           /* ... */
           break;

   case STATE_WAITING: {
           uint32_t delay_ms = 1000;
           /* ... */
           break;
   }
   }

``switch`` jumps to the ``case`` that matches the value. ``break`` leaves the
``switch``. Without ``break``, the code continues into the next case. If you
declare a variable directly in a case, wrap the case in its own ``{ }``.

``enum``
--------

.. code-block:: c

   enum game_state {
           STATE_IDLE,
           STATE_WAITING,
           STATE_REACT,
   };

   enum game_state state = STATE_IDLE;

An ``enum`` gives readable names to a small set of values. Internally they
are numbers (0, 1, 2), but the code reads better.

``struct``
----------

.. code-block:: c

   struct button_event {
           uint32_t timestamp_ms;
           bool pressed;
   };

   struct button_event evt = {
           .timestamp_ms = 1234,
           .pressed = true,
   };

   printk("%u\n", evt.timestamp_ms);

A ``struct`` groups several variables into one. The ``= { .name = value }``
form sets the fields by name. ``evt.timestamp_ms`` reads one field.

Zephyr uses structs everywhere. ``struct gpio_dt_spec`` bundles the GPIO
controller, the pin number and the flags of one LED or button.

Pointers and ``&``
------------------

.. code-block:: c

   gpio_pin_toggle_dt(&led);
   k_msgq_put(&button_msgq, &evt, K_NO_WAIT);

``&led`` means "the address of ``led``", a **pointer** to it. You pass a
pointer when the function must work on *your* variable, and not on a copy of
it. That is why almost every Zephyr call takes ``&something``.

In a function declaration, a ``*`` marks a pointer parameter:
``const struct device *dev`` is "a pointer to a device".

``static``
----------

``static`` has two meanings, depending on where you write it:

- **Outside a function**, on a variable or a function: it is only visible in
  this file. All global variables in the exercises are ``static``.
- **Inside a function**, on a variable: the variable keeps its value between
  calls, and starts at 0. A normal local variable starts fresh on every call.

.. code-block:: c

   static void button_pressed(...)
   {
           static uint32_t press_count;  /* keeps counting */

           press_count++;
   }

Variables that the GPIO driver or the kernel keep a pointer to, such as
``struct gpio_callback``, must be ``static`` (or global): a local variable
disappears when its function returns.

Bits and ``BIT()``
------------------

.. code-block:: c

   gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));

A **bit mask** is a number where each bit stands for one thing, here one pin
of a GPIO controller. ``BIT(n)`` is a number with only bit ``n`` set:
``BIT(0)`` is 1, ``BIT(3)`` is 8, ``BIT(7)`` is 128. So ``BIT(button.pin)``
means "only the button pin".

``printk()`` format strings
---------------------------

.. code-block:: c

   printk("[%6u ms] press %u\n", evt.timestamp_ms, press_count);

``printk()`` prints to the serial console. Each ``%`` placeholder is replaced
by the next value after the string:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Placeholder
     - Prints

   * - ``%d``
     - an ``int`` (can be negative)

   * - ``%u``
     - an unsigned number such as ``uint32_t``

   * - ``%6u``
     - the same, padded to 6 characters

   * - ``%03u``
     - the same, padded with zeros to 3 digits (``7`` becomes ``007``)

   * - ``%ld``
     - a ``long``, for example an ``atomic_t``

   * - ``%s``
     - a text string

``\n`` starts a new line. The compiler checks that the placeholders match the
values, and warns if they don't.
