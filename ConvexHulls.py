from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay

import re

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri

import networkx as nx

class ConvexHulls:
	"""
		v1.0
		This defines a generalized parse dispatcher; 
		All parse functions reside in subclasses.
	"""


	def __init__(self, connected_components=False):
		
		"""
		"""
		self.connected_components = connected_components
		self.vertices = []

		self.getVertices()

		self.makeConvexHull()

		# self.makeDelaunayTriangulation()

		# if not self.connected_components: 
		# 	self.makeDelaunayTriangulation()

		# else:
		# 	self.writeConnectedComponentsTempFile()
			

	def getVertices(self):
		cc_file = open("TempCCVertices.txt", "r")

		for line in cc_file:
			vertices = []
			temp_v = []


			"""
				This part is to save the 105 seconds of reading the file and creating CC. 
				Reading the CC from the temporary file into the rest of the algorithm
				TODO: Integration
			"""

			if line[:1] == "-":
				print "For Surface ID: ", int(line.split()[1])
				
			else:
				temp = re.split(",|\(|\)|\[|\]", line)				
				for each in temp:
					try:
						temp_v.append(float(each))
					except:
						pass

				for x in xrange(0,len(temp_v)-1, 3):
					vertex = [temp_v[x], temp_v[x+1], temp_v[x+2]]
					vertices.append(vertex)

				self.vertices.append(vertices)


	def writeConnectedComponentsTempFile(self):
		cc_file = open("TempCCVertices.txt", 'w')
		
		for index, (c, locs) in enumerate(self.connected_components): 
			if len(c) > 15: 
				tempStr = "---------------- %d ----------------\n"%(index)
				cc_file.write(tempStr)
				cc_file.write(str(c))
				cc_file.write("\n")


	def makeConvexHull(self):

		for eachCC in self.vertices:
			vertices = eachCC

			x = np.array([i[0] for i in vertices])
			y = np.array([i[1] for i in vertices])
			z = np.array([i[2] for i in vertices])
			
			x = x[self.reject_outliers(y)]
			z = z[self.reject_outliers(y)]
			y = y[self.reject_outliers(y)]

			points = np.array([x,z]).T

			hull = ConvexHull(points)
			plt.plot(points[:,0], points[:,1], 'o')

			for simplex in hull.simplices:
				plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
			plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
			plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
			plt.show()

			break



	def makeDelaunayTriangulation(self):

		for eachCC in self.vertices:
			vertices = eachCC
			# hull = ConvexHull(vertices)
			# indices = hull.simplices
			# v = vertices[indices]

			x = np.array([i[0] for i in vertices])
			y = np.array([i[1] for i in vertices])
			z = np.array([i[2] for i in vertices])
			
			x = x[self.reject_outliers(y)]
			z = z[self.reject_outliers(y)]
			y = y[self.reject_outliers(y)]

			tri = Delaunay(np.array([x,z]).T)

			# print 'polyhedron(faces = ['
			# #for vert in tri.triangles:
			# for vert in tri.simplices:
			# 	print '[%d,%d,%d],' % (vert[0],vert[1],vert[2]),
			# print '], points = ['
			# for i in range(x.shape[0]):
			# 	print '[%f,%f,%f],' % (x[i], y[i], z[i]),
			# print ']);'

			fig = plt.figure()
			ax = fig.add_subplot(1, 1, 1, projection='3d')
			ax.plot_trisurf(x, y, z, triangles=tri.simplices, cmap=plt.cm.Spectral)
			plt.show()


			break

	def reject_outliers(self, data, m=2):
		return abs(data - np.mean(data)) < m * np.std(data)






