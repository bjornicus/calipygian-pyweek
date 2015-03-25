# Introduction #

If you haven't set up your environment yet, here's some information on how to do it.

# Installation #

You may want to install all or some of this stuff:

Python 2.6: http://www.python.org/download/releases/2.6/

Pyglet: http://pyglet.org/, pyglet works with Python 2.6 but not 3.1 from my experience.

Eclipse IDE: http://www.eclipse.org/

PyDev: http://pydev.org/download.html Look at the Easy install instructions

Nose (unit testing framework): http://blog.sadphaeton.com/2009/01/20/python-development-windows-part-1installing-python.html

Tortoise SVN: http://tortoisesvn.net/

Google Code in the source tab gives you the https site for the svn. After this, hit the generate password for your password to the svn. After that, you should be good to go.

# Seeing the Project in Eclipse #

If you're using eclipse, you will need to hit the File -> Import and import the .project file in the svn in order for eclipse to open it up correctly.

# Running the Project in Eclipse #

In Eclipse go to Window -> Preferences -> Pydev and set the path to your python install. It will automagically pull in the plugins to python that you have installed.

Click the Rungame.py script and then select Run on eclipse and then select the Python Run config.

# running the unit tests #

Run a cmd window and then in the root directory of the enlistment, just type python nosy.py, the tests will run whenever there's a change to a py file. Very handy!

If you get the numpy.testing.utils not found error, then install numpy from http://sourceforge.net/projects/numpy/files/

# If you hate the colors in Eclipse #
http://srand2.blogspot.com/2009/08/eclipse-color-themes.html