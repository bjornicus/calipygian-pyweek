ENNEAD
===============

Entry in PyWeek #12  <http://www.pyweek.org/12/>
URL: http://calipygian-pyweek.googlecode.com/svn/trunk/pyweek12/
Team: YOUR TEAM NAME (leave the "Team: bit")
Members: Bj�rn Hansen
License: see LICENSE.txt


Running the Game
----------------
You'll need pyglet 1.1 installed (http://www.pyglet.org).

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

