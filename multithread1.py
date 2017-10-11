# -*- coding: utf-8 -*-
import time
import thread
import threading

# 第一类线程
def thread_fcn(args):
    print args, "This is Thread CallBack"
# 但是这样的Thread没有Join效果不好
thread1_ = thread.start_new_thread(thread_fcn, (1, ))

# 第二类线程
class time_thread(threading.Thread):
    exit_flag_ = False
    lock_ = 0;
    def __init__(self, lock__):
        threading.Thread.__init__(self)
        self.lock_ = lock__
        return
    
    def run(self):
        self.exit_flag_ = False
        while True:
            if self.exit_flag_:
                break
            # 上锁
            self.lock_.acquire()
            str_ = time.asctime(time.localtime())
            print str_, threading.Thread.getName(self)
            # 解锁
            self.lock_.release()
            time.sleep(1)
    
    def join(self):
        self.exit_flag_ = True
        threading.Thread.join(self)
    
def test_multi():
    # 创建锁
    locker_ = threading.Lock();
    thread_pool_ = []
    thread_count_ = 10
    for i in range(thread_count_):
        thread_pool_.append(time_thread(locker_))
    for i in range(thread_count_):
        thread_pool_[i].start()
    time.sleep(10)
    for i in range(thread_count_):
        thread_pool_[i].join()
    return thread_pool_
      
if __name__ == '__main__':
    test_multi()
    raw_input("Please Input A String To Exit:")