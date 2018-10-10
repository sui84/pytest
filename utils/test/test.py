from locust import HttpLocust,TaskSet,task

class User1Tasks(TaskSet):
    def on_start(self):
    	print 'do on_start.......'
    	
    @task(1)
    def index1(self):
    	r=self.client.get('/test/index.html')
        print r.text
    @task(2)
    def search1(self):
        r=self.client.get('/test/index.html')
        print r.text

class User1(HttpLocust):
    task_set = User1Tasks
    min_wait = 5000
    max_wait = 9000
    weight = 2