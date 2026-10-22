Before you start
----------------

Do these steps at the start of **every** exercise, even if you already did
them for the previous one. They take one minute and avoid most problems.

**Step 1: connect the board.**
Plug the USB-C cable into the port labeled **MCU-Link** (J21) on the
FRDM-MCXA156 board, and the other end into your PC. This one cable powers the
board, flashes it and carries the serial console.

**Step 2: open a terminal, go to your work directory and activate the virtual
environment.**

.. tabs::

   .. group-tab:: Linux

      Open a terminal (for example with **Ctrl+Alt+T**) and run these two
      commands:

      .. code-block:: bash

         cd ~/zephyr-workdir
         source ~/zephyr-workdir/.venv/bin/activate

      Your prompt must now start with ``(.venv)``. If it does not, the
      ``west`` command will not work.

   .. group-tab:: Windows

      Open **Windows PowerShell** (press the **Win** key, type
      ``powershell``, press **Enter**) and run these three commands:

      .. code-block:: powershell

         cd ~\Desktop\zephyr-workdir
         ~\Desktop\zephyr-workdir\zephyr-workshop\ENV\Scripts\Activate.ps1
         $env:Path += ";C:\NXP\LinkServer_26.9.130"

      Your prompt must now start with ``(ENV)``. If it does not, the ``west``
      command will not work. The last command lets ``west flash`` find
      LinkServer.

Run **all** commands of this exercise in this terminal, without changing the
directory. All file paths on this page are relative to this work directory.
For example, ``zephyr/samples/hello_world/src/main.c`` means:

- Linux: ``~/zephyr-workdir/zephyr/samples/hello_world/src/main.c``
- Windows: ``~\Desktop\zephyr-workdir\zephyr\samples\hello_world\src\main.c``

To check that you are in the right directory, list the samples folder. You
must see folders such as ``basic``, ``hello_world`` and ``workshop``:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         ls zephyr/samples

   .. group-tab:: Windows

      .. code-block:: powershell

         dir zephyr\samples

**Step 3: open the serial console** in a second window and keep it open for
the whole exercise. This is where the board prints its messages.

.. tabs::

   .. group-tab:: Linux

      Open a **second** terminal and run (replace ``ttyACM0`` with your
      device, see :doc:`/flashing_the_board`):

      .. code-block:: bash

         sudo minicom -b 115200 -D /dev/ttyACM0 -8

      To quit minicom later, press **Ctrl+A**, then **X**, then **Enter**.

   .. group-tab:: Windows

      Open **PuTTY**, select **Serial**, type your COM port (for example
      ``COM3``, see :doc:`/flashing_the_board`), set the speed to ``115200``
      and click **Open**.

**Step 4: get your editor ready.** You can use any text editor. These
instructions use **VS Code**. To open a file in VS Code, run ``code`` followed
by the file path in the first terminal, for example:

.. code-block:: bash

   code zephyr/samples/hello_world/src/main.c

These VS Code shortcuts help you follow the instructions:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Shortcut
     - What it does

   * - **Ctrl+F**
     - Find text in the file. Type the text and press **Enter** to jump to
       it. This is how you find the place to edit.

   * - **Ctrl+S**
     - Save the file. **Always save before you build.** A tab with an
       unsaved file shows a white dot ``●`` next to the file name.

   * - **Ctrl+Z**
     - Undo the last change.

How to read the instructions:

- Each step tells you **which file** to open and **where** in it to work: in
  which function, or below which comment. The starter files of exercises 3
  to 5 contain comments named ``Step 1``, ``Step 2``, ... that match the steps
  on the page.
- **"Find ... and change it to ..."** means: press **Ctrl+F**, type the text
  shown, press **Enter**, and replace that text with the new one.
- **"Add ... below ..."** means: find the place, click at the very end of
  that line, press **Enter** and type (or paste) the new lines.
- Do the steps in the order of the page.
- Zephyr code is indented with tabs. If you copy code from this page, the
  indentation may become spaces. That is fine: it still compiles.
