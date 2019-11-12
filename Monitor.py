import psutil
import time
import pyecharts.options as opts
from pyecharts.charts import Line

def line_data(n,delay):
	'''
	生成性能指标数据：
	n代表生成的次数
	delay代表每隔多少秒采集一次
	'''
	TIME=[]
	CPU=[]
	Memory=[]
	Disk=[]
	for i in range(n):
		time.sleep(delay)
		print('正在采集第%s条数据' % str(i+1))
		TIME.append(time.strftime("%H:%M:%S", time.localtime()))
		CPU.append(psutil.cpu_percent())
		Memory.append(psutil.virtual_memory().percent)
		Disk.append(psutil.disk_usage('c:').percent)
	return TIME,CPU,Memory,Disk,n,delay

def line_smooth(TIME,CPU,Memory,Disk,n,delay) -> Line:
	'''
	设置可视化图标格式，生成echarts折线图
	'''
	c = (
		Line()
		.add_xaxis(TIME)
		.add_yaxis("CPU", CPU, is_smooth=True)
		.add_yaxis("Memory", Memory, is_smooth=True)
		.add_yaxis("Disk", Disk, is_smooth=True)
		.set_global_opts(title_opts=opts.TitleOpts(title="资源利用率(%)",subtitle="采集次数：%s  采集频率：%ss/次" % (n,delay))
			,toolbox_opts=opts.ToolboxOpts(is_show=True)
			,datazoom_opts=opts.DataZoomOpts(is_show=True,range_start=60,range_end=100))
	)
	print('成功生成折线图')
	return c

if __name__ == "__main__":
	temp_data=line_data(30,1)
	file_name='Performance_'+time.strftime("%Y%m%d", time.localtime())+'.html'
	line_smooth(temp_data[0],temp_data[1],temp_data[2],temp_data[3],temp_data[4],temp_data[5]).render(file_name)





