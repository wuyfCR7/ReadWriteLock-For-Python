# -*- coding: utf-8 -*-
# wyf 20171011
import threading

# Read Write Lock
class RWLock:
    """
    A simple reader-writer lock Several readers can hold the lock
    simultaneously, XOR one writer. Write locks have priority over reads to
    prevent write starvation. wake up writer accords to FIFO
    """
    _mutex_ = 0;
    _read_allowed_condition_  = 0;
    _write_allowed_condition_ = 0;
    _write_locked_ = False
    _readers_ = 0
    def __init__(self):
        self._mutex_ = threading.Lock()
        self._read_allowed_condition_  = threading.Condition(self._mutex_)
        self._write_allowed_condition_ = threading.Condition(self._mutex_)
        self._write_locked_ = False
        self._readers_ = 0

    def read_acquire(self):
        """Acquire a read-lock. Blocks only if some thread has  acquired write-lock."""
        self._mutex_.acquire()
        while self._write_locked_:
            self._read_allowed_condition_.wait()
        self._readers_ += 1
        self._mutex_.release()

    def read_release(self):
        """Release a read-lock."""
        self._mutex_.acquire()
        self._readers_ -= 1
        if not self._readers_:
            self._write_allowed_condition_.notifyAll()
        self._mutex_.release()

    def write_acquire(self):
        """Acquire a write lock. Blocks until there are no acquired read- or write-locks."""
        self._mutex_.acquire()
        while self._readers_ > 0 | self._write_locked_:
            self._write_allowed_condition_.wait()
        self._write_locked_ = True
        self._mutex_.release()

    def write_release(self):
        """Release a write-lock."""
        self._mutex_.acquire()
        self._write_locked_ = False
        self._write_allowed_condition_.notifyAll()
        self._read_allowed_condition_.notifyAll()
        self._mutex_.release()