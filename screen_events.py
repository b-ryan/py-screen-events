import platform
import threading
import time

mac = platform.system() == 'Darwin'

if mac:
    import Quartz
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

    def event_loop(cbk, sleep_time=1, emit_first=True):
        state = screen_state()
        if emit_first:
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
