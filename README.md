py-screen-events
================

A python library to detect when your screen goes blank or wakes up.

Has been tested on Ubuntu 14.04 and OS X Yosemite using Python 2.7.6.

Usage
=====

Have a callback function triggered whenever the screen is locked or turns off:

```python
from screen_events import ScreenState, event_loop


def callback(state):
    if state == ScreenState.ON:
        print "the screen was unlocked or it turned back on"
    elif state == ScreenState.OFF:
        print "the screen was locked or it turned off"
    else:
        print "this will never happen"

event_loop(callback)
```

To get the current state of the screen:

```python
from screen_events import screen_state

print screen_state()
```


Relevant links
==============

Bug report for GetActive (dbus org.gnome.ScreenSaver) changing in trusty:

https://bugs.launchpad.net/unity/+bug/1342152

Python dbus examples (particularly interesting is INTROSPECTIVE_IFACE):

http://en.wikibooks.org/wiki/Python_Programming/Dbus

Docs for org.gnome.ScreenSaver:

https://people.gnome.org/~mccann/gnome-screensaver/docs/gnome-screensaver.html#gs-method-GetActive
