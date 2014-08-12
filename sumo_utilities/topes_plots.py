# -*- coding: utf-8 -*-
import csv
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np



with open('output/samples.csv', 'rb') as f:
    reader = csv.reader(f)
    data = []
    row_cnt = 0
    for row in reader:
        data.append(row)
        row_cnt +=1

x_len = len(data[0])
y_len = row_cnt
X,Y = np.meshgrid([i for i in range(0,x_len)],[i for i in range(0,y_len)])
#print X,Y
Z = []
for i,row in enumerate(data):
    Z.append([])
    for e in row:
        Z[i].append(float(e))

#print Z
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X, Y, Z)

Z_array = np.array(Z)
Z_array = np.transpose(Z_array)

fig_2 = plt.figure(2)
ax_2 = fig_2.add_subplot(111, projection='3d')
cmap = cm.get_cmap("jet", 3*x_len)
cvals = cmap(np.arange(3*x_len))
#print jetcvals
for z in [i for i in range(0,x_len)]:
    xs = np.arange(y_len)
    ys = Z_array[z,:]
    #print jetcvals[z,:],z
    print cvals[z,:]
    ax_2.bar(xs, ys, zs=z, zdir='y', color=cvals[z*3,:], alpha=0.8)


ax_2.set_xlabel('Distancia')
ax_2.set_ylabel('Tiempo')
ax_2.set_zlabel('Velocidad')

plt.show()
