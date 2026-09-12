.. _linux-setup:

Linux setup guide
=================

This page describes the steps required for setting up the development
infrastructure on a Linux-based machine.

.. warning::

   It is assumed your machine is running **Ubuntu 24.04** or newer. For older
   versions of Ubuntu or other Linux distributions, you may need to follow
   the steps from `here <https://docs.zephyrproject.org/latest/develop/getting_started/installation_linux.html#installation-linux>`__.

Installing dependencies
-----------------------

Make sure your host operating system is up to date by running:

.. code:: bash

   sudo apt-get update && sudo apt-get upgrade

Install the required packages by running:

.. code:: bash

   sudo apt-get install -y git

Cloning the repository
----------------------

Before cloning the workshop repository, make sure you create a work directory:

.. code:: bash

   mkdir -p ~/zephyr-workdir && cd ~/zephyr-workdir

To clone the repository:

.. code:: bash

   git clone https://github.com/NXP-Research/zs-main.git && cd zs-main

Running the setup script
------------------------

To run the setup script [#]_: 

.. code:: bash

   ./scripts/setup.sh

.. note::

   While running, the script may prompt you for your password to install
   some additional packages.

Activating the virtual environment
----------------------------------

Before starting the development process, make sure you activate the python
virtual enviroment created by the **setup.sh** script. To do so, run:

.. code:: bash

   source ~/zephyr-workdir/.venv/bin/activate

.. warning::

   You need to re-do this step each time you open a new terminal session!

To check if the virtual environment has been activated, you can look at
your bash prompt:

.. code:: bash

   (.venv) lmc@playground:~$

If you're missing the **(.venv)** bit, that means the virtual environment is
**NOT** active.

Validating your development environment
---------------------------------------

To make sure your environment is prepared for development, you can try to build
the **hello_world** Zephyr sample:

.. code:: bash

   # make sure you're always in ~/zephyr-workdir when developing!
   cd ~/zephyr-workdir

   west build -p -b frdm_mcxa156/mcxa156 zs-zephyr/samples/hello_world

If the **west** command succeeds, that means you're ready for development!
You can now proceed to the next step, which is :doc:`installing LinkServer <installing_linkserver>`.

.. [#] This script is runs the steps described in Zephyr's official
       documentation. See `here <https://docs.zephyrproject.org/latest/develop/getting_started/index.html>`__
       for more details.
