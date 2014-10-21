#!/usr/bin/env python
import platform
import threading
import time

mac = platform.system() == 'Darwin'
linux = platform.system() == 'Linux'

if mac:
    import Quartz
elif linux:
    import dbus
    from dbus import glib
    from dbus.mainloop.glib import DBusGMainLoop
    import gobject
else:
    raise NotImplemented()


class ScreenState:
    def __init__(self, screen_on):
        self.screen_on = screen_on

    def __eq__(self, other):
        return self.screen_on == other.screen_on

    def __str__(self):
        if self.screen_on:
            return 'Screen on'
        return 'Screen off'

ON = ScreenState(True)
OFF = ScreenState(False)

if mac:
    def screen_state():
        # thanks to http://stackoverflow.com/a/11511419/683436
        d = Quartz.CGSessionCopyCurrentDictionary()
        if d and d.get('CGSSessionScreenIsLocked', 0) == 0 and \
           d.get('kCGSSessionOnConsoleKey', 0) == 1:
            return ON
        return OFF
elif linux:
    DBUS_UNLOCKED = 0
    DBUS_LOCKED = 1

    gobject.threads_init()
    glib.init_threads()

    _bus = dbus.SessionBus()
    _screen_saver = dbus.Interface(_bus.get_object('org.gnome.ScreenSaver',
                                                   '/org/gnome/ScreenSaver'),
                                   'org.gnome.ScreenSaver')
    _session = dbus.Interface(_bus.get_object('com.canonical.Unity',
                                              '/com/canonical/Unity/Session'),
                              'com.canonical.Unity.Session')

    # y = dbus.Interface(x, dbus.INTROSPECTABLE_IFACE)
    # print y
    # print y.Introspect()

    def screen_state():
        if _session.IsLocked():
            return OFF
        return ON if _screen_saver.GetActive() == DBUS_UNLOCKED else OFF

def event_loop(cbk, sleep_time=1, emit_current=True):
    state = screen_state()
    if emit_current:
        cbk(state)
    while True:
        new_state = screen_state()
        if state != new_state:
            cbk(new_state)
            state = new_state
        time.sleep(sleep_time)

if __name__ == '__main__':
    def cbk(state):
        print state
    event_loop(cbk)
