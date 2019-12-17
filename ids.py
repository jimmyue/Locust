import requests
import json
import queue
from locust import HttpLocust,TaskSet,task

class ProcessManage(TaskSet):
	@task
	def DealerData(self):
		try:
			model = self.locust.model_data_queue.get()
		except queue.Empty:
			print('no data run')
			exit(0)

		url='/api/modelDetails/getInfo.do'
		parameter={'requestType':'app','ymDay':'20191212','dealerId':'44E30','modelId':model}
		#name归类不同参数URL接口为一个名称,要不然多少个参数就会在报告中显示多少个接口
		with self.client.get(url,name="/api/modelDetails/getInfo.do",params=parameter,catch_response=True) as response:
			if response.status_code == 200 and response.json()['result_msg']=='执行成功':
				response.success()
			else:
				response.failure(parameter)
				print(response.json())
		self.locust.model_data_queue.put_nowait(model)

class WebsiteUser(HttpLocust):
	task_set = ProcessManage
	host='http://ids.gtmc.com.cn'
	min_wait = 3000
	max_wait = 6000
	model_list=['-1','CMY8G','CMY8H','HLD-T','LEVIN','LEVHV','LEPHV','C-HR','L-YRS','YRS-L','iA5']
	model_data_queue = queue.Queue()
	for i in range(len(model_list)):
		model = model_list[i]
		model_data_queue.put_nowait(model)

if __name__ == "__main__":
	import os
	os.system("locust -f ids.py")



