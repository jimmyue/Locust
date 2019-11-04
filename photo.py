import requests
import json
import queue
from locust import HttpLocust,TaskSet,task

class ImageRecognition(TaskSet):
	@task
	def picture(self):
		try:
			request_file = self.locust.picture_data_queue.get()
		except queue.Empty:
			print('account data run out, test ended.')
			exit(0)
		headers={'token':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMDAyNCIsInNlZ21lbnRfc3RhbmRhcmRfaWQiOiIxIiwidXNlcl9uYW1lIjoiYWRtaW4iLCJvcGVuSWQiOiJ0ZXN0V2VjaGF0IiwiY3VzdF9uYW1lIjoi57O757uf566h55CG5ZGYIiwib3JnSWQiOiIxIiwiaXNzdWVyIjoid2F5cyB0dWFoIEpXVCBJc3N1ZXIgMS4wIiwiZXhwIjoxNjAzNzc4NjIzfQ.cC4J7BOTulLvAyUvMsv8pLHMhwy-3PG5Imto1eH5LMCpD1eW2CwOSwvAG8znlKGnmZN1zx8WZlElvy2_6zkY1A'}
		with self.client.post("/test/cucaInvoice/invoice/uploadPicture",headers=headers,files=request_file,catch_response=True) as response:
			if response.status_code == 200 and response.json()['status']['status']==0:
				response.success()
			else:
				response.failure("life fail:%s" % request_file)
				print(response.json())
		self.locust.picture_data_queue.put_nowait(request_file)

class WebsiteUser(HttpLocust):
	task_set = ImageRecognition
	host='http://iw.waysdata.com'
	min_wait = 3000
	max_wait = 6000
	pic_list=['001.jpg','002.jpg','003.jpg','1028_1.jpg','1028_2.jpg','1028_3.jpg','1028_4.jpg','1028_5.jpg','1028_6.jpg','1028_9.jpg','1028_10.jpg','1028_12.jpg']
	picture_data_queue = queue.Queue()
	for i in range(len(pic_list)):
		request_file = {'file':(pic_list[i],open(pic_list[i],'rb'),'image/jpg')} #上传图片
		picture_data_queue.put_nowait(request_file)
