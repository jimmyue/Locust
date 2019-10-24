# coding=utf-8
import json
import requests
import pandas as pd
import queue
from locust import HttpLocust,TaskSet,task
from sqlalchemy import create_engine

class SalesForecast(TaskSet):
# 业务逻辑：1.先调用Life_count再调用Sales_count；2.只调用Sales_count
# 根据业务逻辑，设定为Life_count：Sales_count=2:3

	@task(2)
	def Life_count(self):
		try:
			body_life = self.locust.life_data_queue.get()   #从队列里取数据
		except queue.Empty:
			print('account data run out, test ended.')
			exit(0)

		header_life = {"Content-type": "application/json"}
		with self.client.post("/Cal-Variable-Service/predict",headers=header_life,data=body_life,catch_response=True) as response:
			if response.status_code == 200 and 'year' in str(response.json()):
				response.success()
			else:
				response.failure("life fail:%s" % body_life)
		self.locust.life_data_queue.put_nowait(body_life)   #队列数据循环完后，重新加入全部数据再循环，去掉此句则在数据循环完后不再循环

	@task(3)
	def Sales_count(self):
		try:
			body_sale = self.locust.sale_data_queue.get()   #从队列里取数据
		except queue.Empty:
			print('account data run out, test ended.')
			exit(0)

		header_sale = {"Content-type": "application/json"} 
		with self.client.post("/Cal-Sales-Service/predict",headers=header_sale,data=body_sale,catch_response=True) as response:
			if response.status_code == 200 and 'ym_id' in str(response.json()):
				response.success()
			else:
				response.failure("sale fail:%s" % body_sale)
		self.locust.sale_data_queue.put_nowait(body_life)   #队列数据循环完后，重新加入全部数据再循环，去掉此句则在数据循环完后不再循环

class WebsiteUser(HttpLocust):
	task_set = SalesForecast
	host='http://172.16.4.139:1337'
	#模拟用户将会在每个任务执行时的等待执行的时间间隔
	min_wait = 3000
	max_wait = 6000

	#Life_count参数化
	con_life=create_engine('mysql+pymysql://RD_DMS:RD_DMS2016@192.168.1.26:3306/ori_dms?charset=utf8')
	lc=pd.read_sql('select t.ver_id,t.smdl_id,t.modelyear,t.launch_date,t.halt_prod_date,t.halt_sale_date,t.changes_id,t.changes_name from dh_lci_ver_stat t join inf_para_comp_smdl l on l.smdl_id=t.smdl_id',con_life)
	model_col=['smdl_id','modelyear','changes_id']
	model=pd.DataFrame(lc,columns = model_col)
	is_duplicate=model.drop_duplicates().values.tolist()   #去重转换成list
	life_data_queue = queue.Queue()   #创建队列
	for modelid in range(len(is_duplicate)):
		lp=lc.loc[(lc['smdl_id']==is_duplicate[modelid][0]) & (lc['modelyear']==is_duplicate[modelid][1]) & (lc['changes_id']==is_duplicate[modelid][2]),['ver_id','smdl_id','modelyear','launch_date','halt_prod_date','halt_sale_date','changes_id','changes_name']]
		data_life = lp.to_json(orient='records', date_format='iso')   #转成json格式
		body_life = json.dumps({"input": data_life})   #将字典形式的数据转化为字符串
		life_data_queue.put_nowait(body_life)   #往队列里存放元素

	#Sales_count参数化
	con_sale=create_engine('mysql+pymysql://RD_DMS:RD_DMS2016@192.168.1.26:3306/ori_dms?charset=utf8')
	ld=pd.read_sql('select smdl_id,smdl_name from inf_para_comp_smdl where smdl_id!=0',con_sale)
	model_col=['smdl_id','smdl_name']
	model=pd.DataFrame(ld,columns = model_col)
	is_duplicate=model.drop_duplicates().values.tolist()   #去重转换成list
	sale_data_queue = queue.Queue()   #创建队列
	for modelid in range(len(is_duplicate)):
		temp_data="[{"+"\"ym_id\":201912,\"year\":2019,\"month\":12,\"sub_my\":null,\"smdl_id\":{},\"smdl_name\":\"阳光\",\"tp_smdl\":0.915971,\"vit_smdl\":0.4975046117,\"mp_smdl\":0.0,\"bp_smdl\":0.016469226699993032,\"cp_smdl\":6.73468,\"pe1_smdl\":null,\"pe2_smdl\":null,\"pe3_smdl\":null,\"pe4_smdl\":null,\"pe5_smdl\":null,\"pe6_smdl\":null,\"pe7_smdl\":null,\"pe8_smdl\":null,\"pe9_smdl\":null,\"pe10_smdl\":null,\"pdt08_smdl\":0.0,\"pdt09_smdl\":0.0,\"pdt10_smdl\":0.0,\"pdt11_smdl\":0.0,\"pdt12_smdl\":0.0,\"pdt13_smdl\":0.0,\"pdt14_smdl\":0.0,\"pdt15_smdl\":0.0,\"pdt16_smdl\":0.0,\"pdt17_smdl\":0.0,\"pdt18_smdl\":1.0,\"pdt19_smdl\":0.0,\"pdt20_smdl\":0.0,\"pdt21_smdl\":0.0,\"pdt22_smdl\":0.0,\"pdt23_smdl\":0.0,\"pdt24_smdl\":0.0,\"pdt25_smdl\":0.0,\"score0_smdl\":0.0,\"score1_smdl\":0.0,\"score2_smdl\":0.0,\"score3_smdl\":0.0,\"score4_smdl\":0.0,\"score5_smdl\":0.0,\"score6_smdl\":0.0,\"score7_smdl\":0.0,\"score8_smdl\":0.0,\"cpv1_smdl\":0.0,\"cpv2_smdl\":0.0,\"cpv3_smdl\":0.0,\"cpv4_smdl\":0.0,\"cpv5_smdl\":0.0,\"cpv6_smdl\":0.0,\"cpv7_smdl\":0.0,\"cpv8_smdl\":0.0,\"cpv9_smdl\":0.0,\"cpv10_smdl\":0.0,\"month1\":0.0,\"month2\":0.0,\"month3\":0.0,\"month4\":0.0,\"month5\":0.0,\"month6\":0.0,\"month7\":0.0,\"month8\":0.0,\"month9\":0.0,\"month10\":0.0,\"month11\":1.0,\"month12\":0.0,\"wdays\":21.0,\"bspr\":0.0,\"aspr\":0.0,\"sprfstv\":0.0,\"dboat\":0.0,\"maut\":0.0,\"trend\":0.0,\"macro1\":2.18836,\"macro2\":2.97553,\"macro3\":19.5326,\"macro4\":-1.22786,\"macro5\":-0.750467,\"macro6\":-0.142345,\"macro7\":-2.06434,\"macro8\":0.0,\"pem1\":null,\"pem2\":null,\"pem3\":null,\"pem4\":null,\"pem5\":null,\"pem6\":null,\"pem7\":null,\"pem8\":null,\"pem9\":null,\"pem10\":null,\"pem11\":null,\"pem12\":null,\"pem13\":null,\"pem14\":null,\"pem15\":null,\"pem16\":null,\"pem17\":null,\"pem18\":null,\"pem19\":null,\"pem20\":null,\"intercept\":1.0,\"ms\":1860000.0".format(is_duplicate[modelid][0])+"}]"
		data_sale={"input_batch": [temp_data]}
		body = json.dumps(data_sale)   #将字典形式的数据转化为字符串
		sale_data_queue.put_nowait(body_life)   #往队列里存放元素

if __name__ == "__main__":
	import os
	os.system("locust -f mysql_pandas.py")



