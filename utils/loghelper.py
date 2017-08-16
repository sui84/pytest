#encoding=utf-8
import functools
import logging
import confhelper

    
def exception(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
 
    @param logger: The logging object
    """
 
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
    
    
def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("testlogger")
    logger.setLevel(logging.INFO)
    
    conf = confhelper.ConfHelper()
    logpath = conf.GetConfig("filepath","logpath")
    # create the logging file handler
    fh = logging.FileHandler(logpath)
 
    fmt = '[%(asctime)s - %(name)s - %(levelname)s %(process)d %(processName)s %(thread)d %(threadName)s] %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger

logger = create_logger()
@exception(logger)
def zero_divide(i,j):
    i/j

if __name__ == '__main__':
    #zero_divide(1,0)
    zero_divide(1,1)
