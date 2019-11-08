import psutil
import time
import matplotlib.pyplot as plt
import numpy as np

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 500)
y = np.sin(x)
fig, ax = plt.subplots()
# Using set_dashes() to modify dashing of an existing line
line1, = ax.plot(x, y, label='Using set_dashes()')
line1.set_dashes([2, 2, 10, 2])  # 2pt line, 2pt break, 10pt line, 2pt break
# Using plot(..., dashes=...) to set the dashing when creating a line
line2, = ax.plot(x, y - 0.2, dashes=[6, 2], label='Using the dashes parameter')
ax.legend()
plt.show()

#print(psutil.test())
# delay=3
# print('CPU使用率  内存使用率  C盘使用率')
# while True:
# 	time.sleep(delay)
# 	print(' '+str(psutil.cpu_percent())+'%       '\
# 		+str(psutil.virtual_memory().percent)+'%      '\
# 		+str(psutil.disk_usage('c:').percent)+'%')

