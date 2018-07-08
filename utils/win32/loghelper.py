import logging
import inspect
import os

def get_logger(category,lfile):

    logger = logging.getLogger(category)
    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))
    handler = logging.FileHandler(lfile) # os.path.join(dirpath, "service.log"))

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

if __name__=='__main__':
    print __file__
    exit(0)
