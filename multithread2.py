# -*- coding: utf-8 -*-
# 读写锁检测 wyf 20171011
import rwlock
import threading
import time        
val = 0
class WriteThread(threading.Thread):
    rwlocker_  = 0
    exit_flag_ = False
    def __init__(self, rwlocker__):
        self.rwlocker_ = rwlocker__
        threading.Thread.__init__(self)
    
    def run(self):
        global val
        while True:
            if self.exit_flag_:
                break
            self.rwlocker_.write_acquire()
            val += 1
            self.rwlocker_.write_release()
            time.sleep(0.03)
            
    def join(self):
        self.exit_flag_ = True
        threading.Thread.join(self)
        
class ReadThread(threading.Thread):
    rwlocker_  = 0;
    exit_flag_ = False
    cout_locker_ = 0
    def __init__(self, rwlocker__, cout_locker__):
        self.rwlocker_ = rwlocker__
        self.cout_locker_ = cout_locker__
        threading.Thread.__init__(self)
    
    def run(self):
        global val
        while True:
            if self.exit_flag_:
                break
            self.rwlocker_.read_acquire()
            val_copy_ = val
            self.rwlocker_.read_release()
            self.cout_locker_.acquire()
            print self.getName(), val_copy_
            self.cout_locker_.release()
            time.sleep(0.05)
            
    def join(self):
        self.exit_flag_ = True
        threading.Thread.join(self)
        
if __name__ == "__main__":
    read_thread_pool_ = []
    write_thread_pool_ = []
    read_count_ = 10
    write_count_ = 10
    rwlocker_ = rwlock.RWLock()
    cout_locker_ = threading.Lock()
    for i in range(read_count_/2):
        read_thread_pool_.append(ReadThread(rwlocker_, cout_locker_))
    for i in range(write_count_):
        write_thread_pool_.append(WriteThread(rwlocker_))    
    for i in range(read_count_/2):
        read_thread_pool_.append(ReadThread(rwlocker_, cout_locker_))
    for i in range(write_count_):
        write_thread_pool_[i].start()
    for i in range(read_count_):
        read_thread_pool_[i].start()
    time.sleep(10) 
    for i in range(write_count_):
        write_thread_pool_[i].join()
    for i in range(read_count_):
        read_thread_pool_[i].join()