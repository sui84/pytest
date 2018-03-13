#encoding=utf-8
import logging

#LOGPATH = '/storage/emulated/0/qpython/scripts/log.txt'
LOGPATH = r"d:\temp\log.txt"
    
def exception(logger):
    def decorator(func):
 
        def wrapper(*args, **kwargs):
            try:
                msg = "funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                logger.info(msg)
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "exception : funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                logger.exception(err)
 
            # re-raise the exception
            raise
        return wrapper
    return decorator
    
    
def create_logger(logpath):
    logger = logging.getLogger("testlogger")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logpath)
    fmt = '[%(asctime)s - %(name)s - %(levelname)s %(process)d %(processName)s %(thread)d %(threadName)s] %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger

logger = create_logger(LOGPATH)
@exception(logger)
def zero_divide(i,j):
    i/j

if __name__ == '__main__':
    #zero_divide(1,0)
    zero_divide(1,1)
