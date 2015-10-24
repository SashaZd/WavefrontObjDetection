import re
import numpy as np
import math
from ThreeDObject import ThreeDObject
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

class Parser(object):
	"""
		v1.0
		This defines a generalized parse dispatcher; 
		All parse functions reside in subclasses.

		v1.01
		NOTE: New optimization. Since MS Kinect creates a new face for each vertex,
		and does not reuse vertices, we can avoid reading the part of the file that 
		contains information about the faces
		Time before optimization: 4min approx
		Time after  optimization: 3min approx

		File size decrease by deleting normals 

		v1.02 
		Running a K-Means clustering adapted with the assumption about the data (data is
		about the size of -1.0)
		Created a face dictionary that stores the vn and the v
		Only running on faces that are close to normal
		Grouped the faces into fgroups which work on k-means

		v1.03
		---------
		@cjds WORKING ON IT
		Using the Rotating Caliper algorithm to create a bounding box that we can
		use with convex objects

		TODO:
		- If someone can figure out how to run the file reading from the vn 
		  instead of v, we can move much faster by not botherihat tto parse extra v

	"""

	def __init__(self, file_name):
		self.file_name = file_name
		self.v = {} 
		self.fgroups={}; #The dictionary that groups the faces into multiple clusters
		self.vn = {}
		self.f=[]
		self.VNIndex=0 #An inde for the vertext normals
		self.numberOfSkips=0	
		#self.read_file(file_name)

		# return (self,.v, self.vn, self.f)

	def read_file(self, file_name):
	   	objFile = open(file_name, 'r')
	   	#if the parse function returns false we stop parsing
	   	#this is because we have to reach the faces
	   	for line in objFile:
		   	if not self.parse(line):
		   		break;

		print "Generating Faces"
		#reparse to group into faces
		self.generate_faces()
		print len(self.f)

		"""
		K-Means :
		Changes included are around the threshold separator between clusters
		If any item in the list haas a greater distance than that in returnMeanGroup
		we should make a new cluster around it. 

		Ideally we should run the algorthm repeatedly till acheiving a stable mean centers
		BUT for performance reasons I run this once

		"""
		#a dictionary storing the means
		means={}
		#an array storing the ids of the means
		meanIDs=[]
		print "Splitting by the Y Axis"
		self.fgroups=self.adaptedKMeans(self.f,1)

		groups=[]
		print "Splitting by the X Axis"
		for fgroup in self.fgroups.itervalues():
			groups.append(self.adaptedKMeans(fgroup,2))

		
		print "Save in file"
		#
		return groups
		# index=0
		# for fgroups in groups:
		# 	for fgroup in fgroups.itervalues():
		# 		index+=1
		# 		if(len(fgroup)>500): 
									
					#self.write_file_from_f_group(fgroup,'file-layer'+str(index)+'.obj')

	def bounding_box(self,fgroup):
		max_x=-100
		max_y=-100
		min_x=-100
		min_y=-100
		zAvg=0
		for face in fgroup:
			for v in face.v:
				if(v[0]<min_x):
					min_x=v[0]
				if(v[0]>max_x):
					max_x=v[0]
				if(v[1]<min_y):
					min_y=v[1]
				if(v[1]>max_y):
					max_y=v[1]
				zAvg+=v[2]/3
		zAvg/=len(fgroup)
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		X, Y = np.meshgrid(np.array([min_x, max_x]), np.array([min_y,max_y]))
		Z=np.array([zAvg,zAvg])
		surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
        plt.show()


	def adaptedKMeans(self,fgroup,axis):
		#a dictionary storing the means
		means={}
		#an array storing the ids of the means
		fgroups={}
		for face in fgroup:
			#get the ID in meanIDs that best represents this point
			meanID=self.returnMeanGroup(means,face.v[2][axis])
			if(meanID==-1):
				size=len(fgroups)
				fgroups[size+1]=[]
				fgroups[size+1].append(face)
				means[size+1]=face.v[2][axis]
			else:
				fgroups[meanID].append(face)
				means[meanID]=self.recalculate(means[meanID],face.v[2][axis],fgroups[meanID],axis)

		return fgroups

	#recalculation of the mean
	def recalculate(self,cmean,current,fgroup,axis):
		length=len(fgroup)
		mean=cmean*(length-1)+current
		mean/=length
		return mean

	#returning the mean group id of the group that it belongs to.
	#
	def returnMeanGroup(self,means,value):
		difference=0.1
		currentMean=-1
		for meanID in means.iterkeys():
			if(math.fabs(value-means[meanID])<difference):
				difference=math.fabs(value-means[meanID])
				currentMean=meanID
		return currentMean
	
	def write_file_from_f_group(self,fgroup,output_file_name):
		outputFile = open(output_file_name, 'w')
		
		for face in fgroup:
			for v in (face.v):
				outStr = "v " + " ".join(str(x) for x in v) + "\n"
				outputFile.write(outStr)

		for face in fgroup:
			for vn in (face.vn):
				outStr = "vn " + " ".join(str(x) for x in vn) + "\n"
				outputFile.write(outStr)

		for k in range(len(fgroup)):
			outStr = "f " + str(3*k+1)+ "//" +  str(3*k+1) + " " + str(3*k+2) + "//" +  str(3*k+2) + " " + str(3*k+3) + "//" +  str(3*k+3) + "\n";
			outputFile.write(outStr)


	def write_file(self,output_file_name):
		outputFile = open(output_file_name, 'w')
		for key in (self.v.keys()):
			outStr = "v " + " ".join(str(x) for x in self.v[key]) + "\n"
			outputFile.write(outStr)

		for key in (self.vn.keys()):
			outStr = "vn " + " ".join(str(x) for x in self.vn[key]) + "\n"
			outputFile.write(outStr)

		#print all the numbers from 1 onwards
		for k in range(len(self.vn.keys())/3):
			outStr = "f " + str(3*k+1)+ "//" +  str(3*k+1) + " " + str(3*k+2) + "//" +  str(3*k+2) + " " + str(3*k+3) + "//" +  str(3*k+3) + "\n";
			outputFile.write(outStr)

	def generate_faces(self):
		#make faces available to memory
		vnkeys= sorted(self.vn.keys())
		prev2=0;
		for k in range(len(vnkeys)/3):
			v=[]
			v.append(self.v[vnkeys[3*k]])
			v.append(self.v[vnkeys[3*k+1]])
			v.append(self.v[vnkeys[3*k+2]])
			# if prev2>v[2][2]:
			# 	print v[2][2]
			# 	print prev2
			# 	print vnkeys[3*k]
			# 	print vnkeys[3*k+1]
			# 	print vnkeys[3*k+2]
			# 	raw_input()
			prev2=v[2][2]
			vn=[]
			vn.append(self.vn[vnkeys[3*k]])
			vn.append(self.vn[vnkeys[3*k+1]])
			vn.append(self.vn[vnkeys[3*k+2]])
			self.f.append(ThreeDObject(v,vn))

	def parse(self, line):
	   	"""Determine what type of line we are and dispatch appropriately."""
	   
   		if line[0:2] == "#":
			pass;

		elif line[0:2] == "v ":
			self.parse_v(line)

		elif line[0:2] == "vn":
			self.parse_vn(line)

		elif line[0:2] == "f ":
			return False

		return True

	def parse_v(self, line):
		currentInd=len(self.v)+1 
		xyz = tuple(map(float, line.split()[1:]))
		# if(currentInd>1):
		# 	if(math.fabs(xyz[2]-self.v[currentInd-1][2])>0.2):
		# 		print self.v[currentInd-1][2]
		# 		print xyz[2]
		# 		print "-------"
		# 		print line
		# 		raw_input()

		self.v[currentInd]=xyz


	"""
	parse_vn does the test for which vertices to keep or not according to the angles formed
	with the y axis.

	If it detects something that doesn't fit in it removes all three normals from the pattern. 
	as the face won't exist

	We have a counter variable called self.VNIndex. 
	VNIndex % 3 will give the number of future numbers to skip

	"""
	def parse_vn(self, line):
		#Using self.VNIndex so that we can delete the extra normals 
		self.VNIndex=self.VNIndex+1
		#If we have to skip this don't bother to check
		if self.numberOfSkips!=0:
			self.numberOfSkips-=1
			return

		xyz = tuple(map(float, line.split()[1:]))
		#Only keep faces where the y-vector normals < 20 radians
		#0.174533
		if (self.angle_with_y(xyz) <= 0.174533*2):
			self.vn[self.VNIndex]=(xyz)
		else:
			self.numberOfSkips=(3-(self.VNIndex%3))%3
			
			##remove extra vn
			for i in range(1,3-self.numberOfSkips):
				self.vn.pop(self.VNIndex-i,None)	
			##remove extra v
			#for i in range(self.numberOfSkips-2,self.numberOfSkips+1):
			#	self.v.pop(self.VNIndex+i,None)	

	def angle_with_y(self,v1):
		"""Dot product, then normalize, then offset from origin"""
		v2=[0,1,0]
		
		cosang = np.dot(v1, v2)
		sinang = np.linalg.norm(np.cross(v1, v2))
		return np.arctan2(sinang, cosang)

	def angle_with_z(self,v1):
		"""Dot product, then normalize, then offset from origin"""
		v2=[0,0,1]
		cosang = np.dot(v1, v2)
		sinang = np.linalg.norm(np.cross(v1, v2))
		return np.arctan2(sinang, cosang)

