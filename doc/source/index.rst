Welcome to NXP's Zephyr workshop!
=================================

About
-----

This is a hands-on, beginner-friendly introduction to
`Zephyr <https://www.zephyrproject.org/>`__, an open source, scalable
real-time operating system (RTOS) for resource-constrained and embedded
devices. You write, build and flash real code on an NXP **FRDM-MCXA156**
development board, and you see the result on its LEDs, buttons and serial
console.

**Who is it for?**
Developers who are new to Zephyr or to RTOS-based development. You do not
need prior Zephyr experience. If you are rusty on C, the
:doc:`C primer <exercises/c_primer>` covers what you need, and the
:doc:`glossary <exercises/glossary>` explains the terminology.

**What will you learn?**
You go from "Hello World" to a small reaction-time game, one core concept per
exercise:

- the structure of a Zephyr application and the ``west`` build tool
- controlling hardware with GPIO, described by Devicetree and configured with
  Kconfig
- reacting to events with interrupts and callbacks
- running work concurrently with threads, priorities and message queues
- combining timing, synchronization and a state machine in a complete
  application

**What do you need?**
A PC running Linux or Windows, an FRDM-MCXA156 board and a USB-C cable. The
:doc:`infrastructure guide <infrastructure/index>` walks you through the
software setup. Complete the setup before the exercises start, so you can
spend the workshop time on Zephyr itself.

**How is it organized?**
Each exercise builds on the previous one, but every page is self-contained.
Exercises 3 to 5 come with a starter project and a working solution, so you
can always catch up if you get stuck.

Getting started
---------------

Check out the following resources to help you get started:

- ✅ :doc:`Infrastructure getting started <infrastructure/index>`
- ✅ :doc:`Flashing your Zephyr application <flashing_the_board>`

Exercises
---------

Once your setup works, go through the exercises in order:

- :doc:`Introduction <exercises/index>`
- :doc:`Exercise 1: Hello Zephyr <exercises/01_hello_world>`
- :doc:`Exercise 2: Blinky <exercises/02_blinky>`
- :doc:`Exercise 3: Button + LED <exercises/03_button>`
- :doc:`Exercise 4: Threads <exercises/04_threads>`
- :doc:`Exercise 5: Reaction Game <exercises/05_reaction_game>`

New to C or to embedded software? Keep these two pages open while you work:

- :doc:`The C you need <exercises/c_primer>`
- :doc:`Glossary <exercises/glossary>`

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Getting started

   flashing_the_board
   infrastructure/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Exercises

   exercises/index
   exercises/01_hello_world
   exercises/02_blinky
   exercises/03_button
   exercises/04_threads
   exercises/05_reaction_game

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Reference

   exercises/c_primer
   exercises/glossary
