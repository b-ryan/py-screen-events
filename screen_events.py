#!/usr/bin/env python
import platform
import threading
import time


class ScreenState:
    ON = 1
    OFF = 2

if platform.system() == 'Darwin':
    import Quartz

    def screen_state():
        # thanks to http://stackoverflow.com/a/11511419/683436
        d = Quartz.CGSessionCopyCurrentDictionary()
        if d and d.get('CGSSessionScreenIsLocked', 0) == 0 and \
           d.get('kCGSSessionOnConsoleKey', 0) == 1:
            return ScreenState.ON
        return ScreenState.OFF

elif platform.system() == 'Linux':
    import dbus
    from dbus import glib
    from dbus.mainloop.glib import DBusGMainLoop
    import gobject

    _DBUS_UNLOCKED = 0
    _DBUS_LOCKED = 1

    gobject.threads_init()
    glib.init_threads()

    _bus = dbus.SessionBus()
    _screen_saver = dbus.Interface(_bus.get_object('org.gnome.ScreenSaver',
                                                   '/org/gnome/ScreenSaver'),
                                   'org.gnome.ScreenSaver')
    _session = dbus.Interface(_bus.get_object('com.canonical.Unity',
                                              '/com/canonical/Unity/Session'),
                              'com.canonical.Unity.Session')

    def screen_state():
        if _session.IsLocked():
            return ScreenState.OFF
        return ScreenState.ON \
            if _screen_saver.GetActive() == _DBUS_UNLOCKED \
            else ScreenState.OFF

else:
    raise NotImplemented()


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
        if state == ScreenState.ON:
            print 'on'
        elif state == ScreenState.OFF:
            print 'off'
        else:
            print 'unknown'
    event_loop(cbk)
