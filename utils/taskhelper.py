from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import traceback
import datetime

class TaskHelper(object):
    def __init__(self,host="localhost",user="",pwd="",db="test"):
        self.host = host
        self.port = 27017
        self.client = MongoClient(self.host, self.port)

        self.jobstores = {
            'mongo': MongoDBJobStore(collection='job', database='test', client=self.client),
            'default': MemoryJobStore()
        }
        self.executors = {
            'default': ThreadPoolExecutor(10),
            'processpool': ProcessPoolExecutor(3)
        }
        self.job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        #self.scheduler = BlockingScheduler(jobstores=self.jobstores, executors=self.executors, job_defaults=self.job_defaults)
        self.scheduler = BackgroundScheduler(jobstores=self.jobstores, executors=self.executors, job_defaults=self.job_defaults)

    def AddJob(self,job):
        self.scheduler.add_job(job, 'interval', seconds=5)

    def AddOnetimeJob(self,job):
        self.scheduler.add_job(job, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1))

    def AddDailyJob(self,job):
        #self.scheduler.add_job(job, 'date', run_date=datetime(2017,8, 20), args=['text'])
        print 'ddd'

    def Start(self):
        print "Task Start"
        self.scheduler.start()

    def Stop(self):
        print "Task Stop"
        self.scheduler.job.Job.pause()
        self.scheduler.schedulers.base.BaseScheduler.pause_job()

    def Resume(self):
        print "Task Resume"
        self.scheduler.job.Job.resume()
        self.scheduler.schedulers.base.BaseScheduler.resume_job()

def my_job():
    print 'hello world'

if __name__ == '__main__':
    task = TaskHelper()
    task.AddOnetimeJob(my_job)
    try:
        task.Start()
        #task.Stop()
        #task.Resume()
        #task.Stop()
    except Exception,e:
        print 'Error:',e.message,'\n',traceback.format_exc()
