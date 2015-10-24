import numpy as np
import math
from Parser import Parser
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D


file_name = 'Chair.obj'
output_file_name = "LargeView2.obj"


""" 
	Returns an object that contains 3 dictionaries: v, vn, f
	v[index] will give you the vertice coordinates at that index
	vn[index] will give you the vector normals (from origin) at that index
	f[index] will give you the face in the format (vx, vnx, vy, vny, vz, vnz) where f = vx//vnx vy//vny vz//vnz  
"""

#outputFile = open(output_file_name, 'w')
parsedObj = Parser(file_name)
# print parsedObj.v[1]
#parsedObj.write_file(output_file_name)
#bounding_box()
groups=parsedObj.read_file(file_name)


zAvg=0
fig = plt.figure()
ax = fig.gca(projection='3d')
for fgroups in groups:
	for fgroup in fgroups.itervalues():
		max_x=-100
		max_y=-100
		min_x=100
		min_y=100
		if(len(fgroup)>600):
			for face in fgroup:
				for v in face.v:
					if(v[0]<min_x):
						min_x=v[0]
					if(v[0]>max_x): 
					if(v[1]<min_y):
						min_y=v[1]
					if(v[1]>max_y):
						max_y=v[1]
					zAvg+=v[2]/3
			zAvg/=len(groups[0][1])
			X, Y = np.meshgrid(np.array([min_x, max_x]), np.array([min_y,max_y]))
			Z=np.array([zAvg,zAvg])
			surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)

plt.show()
