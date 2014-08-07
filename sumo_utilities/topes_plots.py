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
jetcmap = cm.get_cmap("winter", 3)
jetcvals = jetcmap(np.arange(3))
#print jetcvals[3,:]
for z in [i for i in range(0,x_len)]:
    xs = np.arange(y_len)
    ys = Z_array[z,:]
    ax_2.bar(xs, ys, zs=z, zdir='y', color=jetcvals[z-1,:], alpha=0.8)

# for c, z in zip(['r', 'g', 'b', 'y'], [i for i in range(0,x_len)]):
#     xs = np.arange(y_len)
#     ys = Z_array[z,:]
#     print c
#     ax_2.bar(xs, ys, zs=z, zdir='y', color=jetcvals[z-1,:], alpha=0.8)
    #print Z[z]

# print xs
# print ys

ax_2.set_xlabel('Distancia')
ax_2.set_ylabel('Tiempo')
ax_2.set_zlabel('Velocidad')

plt.show()
# X = np.array([[0,1,2,3,4],[0,1,2,3,4]])  # lenght N
# Y = np.array([[0,1,2,3,4],[0,1,2,3,4]])  # lenght M
# Z = np.array([[1,1,1,1,1],[1,1,1,1,1]])  # M x N
# #X, Y = np.meshgrid(X, Y)
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
# plt.show()



# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# X, Y, Z = axes3d.get_test_data(0.05)
# print X
# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
#
# plt.show()
