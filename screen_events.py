import platform
import threading
import time

mac = platform.system() == 'Darwin'

if mac:
    import Quartz
else:
    raise NotImplemented()

noop = lambda: null


class ScreenListenerThread(threading.Thread):
    def __init__(self, locked_cbk=noop, unlocked_cbk=noop, sleep_time=1):
        super(ScreenListenerThread, self).__init__()
        self.daemon = True
        self._locked_cbk = locked_cbk
        self._unlocked_cbk = unlocked_cbk
        self._sleep_time = sleep_time

    def _mac_status(self):
        # thanks to http://stackoverflow.com/a/11511419/683436
        d = Quartz.CGSessionCopyCurrentDictionary()
        if d and d.get('CGSSessionScreenIsLocked', 0) == 0 and \
           d.get('kCGSSessionOnConsoleKey', 0) == 1:
            return 'unlocked'
        return 'locked'

    def _run_mac(self):
        status = self._mac_status()
        while True:
            new_status = self._mac_status()
            if status != new_status:
                if new_status == 'unlocked':
                    self._unlocked_cbk()
                else:
                    self._locked_cbk()
                status = new_status
            time.sleep(self._sleep_time)

    def run(self):
        if mac:
            self._run_mac()
        else:
            raise NotImplemented()


if __name__ == '__main__':
    def locked():
        print "locked"

    def unlocked():
        print "unlocked"

    t = ScreenListenerThread(locked, unlocked)
    t.start()
    while True:
        pass
