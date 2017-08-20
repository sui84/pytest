#coding=utf-8
import time
import traceback
import sys

if __name__ == '__main__':
    print time.ctime(), 'Start...'
    try:
        if len(sys.argv) > 1:
            print sys.argv[1]
    except Exception,e:
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
    finally:
        print time.ctime(), 'Done!'

