#encoding=utf-8
import multiprocessing

def writer_proc(q):
    try:
        for i in range(0,10):
            q.put(i,block = False)    #这个block的选项要加上，默认block为True，读不到就阻塞，会让人感觉像死锁了一样，而操作没有成功会抛出Queue.Full的异常，所以要处理一下
            print "write :",i
    except:       
        pass 
def reader_proc(q):
    try:       
        value = q.get(block = False)  #这个block的选项要加上，默认block为True，读不到就阻塞，会让人感觉像死锁了一样，而操作没有成功会抛出Queue.Full的异常，所以要处理一下
        print "read :", value
    except:
        pass

if __name__ == '__main__':
    q = multiprocessing.Queue()
    reader = multiprocessing.Process(target=reader_proc,args=(q,))
    reader.start()
    writer = multiprocessing.Process(target=writer_proc,args=(q,))
    writer.start()
    reader.join()
    writer.join()
