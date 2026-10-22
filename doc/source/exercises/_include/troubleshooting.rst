If something goes wrong
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Problem
     - What to do

   * - ``west: command not found`` (Linux) or ``west : The term 'west' is not
       recognized`` (Windows)
     - The virtual environment is not active. Repeat step 2 of
       `Before you start`_.

   * - ``ERROR: Build directory "..." is for application "...", but source
       directory "..." was specified``
     - The ``build`` folder still contains another application. Run the full
       ``west build -p -b frdm_mcxa156/mcxa156 ...`` command again, **with**
       ``-p``.

   * - The build fails with ``error:`` messages
     - Scroll up to the **first** line that contains ``error:``. It looks like
       ``.../src/main.c:19:9: error: ...``: the file, the **line** (19) and
       the column (9) of the problem. In VS Code, press **Ctrl+G**, type the line
       number and press **Enter** to go to that line. Common causes: a
       missing ``;`` at the end of a line, a missing ``}``, or a typo in a
       name. Fix it, save, build again.

   * - You changed the code, but the board still does the old thing
     - Did you save the file (**Ctrl+S**)? Did you run ``west build`` *and*
       ``west flash`` again?

   * - ``west flash`` fails
     - Check that the cable is in the **MCU-Link** port (J21). Unplug the
       cable and plug it in again. On Windows, check that you ran the
       ``$env:Path += ...`` command from step 2 in this terminal.

   * - Nothing appears in the serial console
     - Check the port (``ttyACM0`` / ``COM3``) and the speed (``115200``).
       Then press the **RESET** button on the board: the application starts
       again from the beginning.

   * - You broke the file and want to start over
     - Restore the original files of the application folder with ``git``
       (see the commands in `Start over`_). This **deletes all your
       changes** in that folder, and the files you created there. It cannot
       be undone.
