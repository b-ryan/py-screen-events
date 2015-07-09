#!/usr/bin/env python
import platform
import threading
import time


class ScreenState:
    ON = 1
    OFF = 2

if platform.system() == 'Darwin':
    import Quartz

    def init():
        pass

    def screen_state(context):
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

    class DbusEnvironment:
        def __init__(self):
            gobject.threads_init()
            glib.init_threads()

            bus = dbus.SessionBus()

            self.screen_saver = dbus.Interface(
                bus.get_object('org.gnome.ScreenSaver',
                               '/org/gnome/ScreenSaver'),
                'org.gnome.ScreenSaver')

            try:
                self.session = dbus.Interface(
                    bus.get_object('com.canonical.Unity',
                                   '/com/canonical/Unity/Session'),
                    'com.canonical.Unity.Session')

                self.is_session_locked = self._unity__is_session_locked
            except Exception:
                self.session = dbus.Interface(
                    bus.get_object('org.gnome.SessionManager',
                                   '/org/gnome/SessionManager'),
                    'org.gnome.SessionManager')
                self.is_session_locked = self._gnome__is_session_locked


        def _unity__is_session_locked(self):
            return self.session.IsLocked()

        def _gnome__is_session_locked(self):
            return not self.session.IsSessionRunning()

        def is_screen_saver_on(self):
            return self.screen_saver.GetActive()

    def init():
        return DbusEnvironment()

    def screen_state(environment):
        if environment.is_session_locked():
            return ScreenState.OFF

        if environment.is_screen_saver_on():
            return ScreenState.OFF

        return ScreenState.ON

else:
    raise NotImplemented()


def event_loop(cbk, sleep_time=1, emit_current=True):
    environment = init()
    state = screen_state(environment)
    if emit_current:
        cbk(state)
    while True:
        new_state = screen_state(environment)
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
