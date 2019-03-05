import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print('vector')

ax = plt.subplot(111, projection='3d')
ax.set_zlabel('Z')  # 坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')


# 点数据

#3-1
p11 = [516152.52,4010933.13,172.90]
p12 = [516156.17,4010931.36,169.78]
p13 = [516152.91,4010931.99,166.43]
#3-2
p21 = [516155.77,4010883.46,174.30]
p22 = [516154.71,4010883.45,171.05]
p23 = [516153.82,4010883.61,166.98]

xdata = [152.52,156.17,152.91]
ydata = [133.13,131.36,131.99]
zdata = [72.9,69.78,66.43]
ax.scatter3D(xdata, ydata, zdata, c='y')

xdata = [155.77,154.71,153.82]
ydata = [83.46,83.45,83.61]
zdata = [74.3,71.05,66.98]
ax.scatter3D(xdata, ydata, zdata, c='g')

#planPoint red
xdata = [162.49]
ydata = [133.78]
zdata = [73.18]
ax.scatter3D(xdata, ydata, zdata, c='r')


#三维线的数据
#PQ1
xline = [152.52,155.77]
yline = [133.13,83.46]
zline = [72.9,74.3]
ax.plot3D(xline, yline, zline, 'gray')

xline = [0,3.25]
yline = [0,-49.67]
zline = [0,1.4]
ax.plot3D(xline, yline, zline, 'y')

#PQ2
xline = [0,9.975]
yline = [0,0.65266]
zline = [0,-0.28]
ax.plot3D(xline, yline, zline, 'r')

#lineDirection
xline = [0,9.97]
yline = [0,0.65]
zline = [0,5.10]
ax.plot3D(xline, yline, zline, 'g')

#曝光点
xdata = [162.85]
ydata = [132.17]
zdata = [71.34]
ax.scatter3D(xdata, ydata, zdata, c='y')


plt.show()
