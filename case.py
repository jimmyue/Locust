from locust import Locust,TaskSet,task,TaskSequence,seq_task

#设定任务权重      @task(n)
#设定任务顺序      @seq_task(n)
#设定locust类权重  weight=n

class WebTaskSet(TaskSet):
	@task(3)
	class web_task1(TaskSet):
		@task(2)
		def web_task1_sub1(self):
			print("executing web_task1_sub1")
		@task(1)
		def web_task1_sub2(self):
			print("executing web_task1_sub2")

	@task(6)
	def web_task2(self):
		print("executing web_task2")


class MobileTaskSet(TaskSequence):
	@seq_task(1)
	def Mobile_task1(self):
		print("executing Mobile_task1")

	@seq_task(2)
	def Mobile_task2(self):
		print("executing Mobile_task2")

	@seq_task(3)
	@task(10)
	def Mobile_task3(self):
		print("executing Mobile_task3")


class WebUserLocust(Locust):
	host='https://www.baidu.com/'
	weight = 2
	task_set = WebTaskSet
	min_wait = 3000
	max_wait = 6000

class MobileUserLocust(Locust):
	host='https://www.baidu.com/'
	weight = 1
	task_set = MobileTaskSet
	min_wait = 5000
	max_wait = 15000

if __name__ == "__main__":
	import os
	os.system("locust -f case.py WebUserLocust MobileUserLocust")