import re
import numpy as np
import math

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

		v1.02 Still Ongoing
		-------------------
		Attempting to do a heirarchial cluster on the faces that we want.
		Assuming that a face is a combination of an objects v and vn.
		Only running on faces that are close to normal
		CANCELLED
		Using the Rotating Caliper algorithm to create a bounding box that we can
		use.

		ASSUMPTIONS:
		- The z-index goes from a lowwe negative level to a higher negative level
		in the OBJ file


		TODO:
		- If someone can figure out how to run the file reading from the vn 
		  instead of v, we can move much faster by not bothering to parse extra v
		- I've noticed that every 3 normals, have similar values. Maybe, we can skip
		  extra work by only reading one and skipping the other two if it is negative
		- Replace negative y look with the following code because it is a better test 
			for an angle math.degrees(self.angle_with_y(self.vn[1]))

	"""

	def __init__(self, file_name):
		self.file_name = file_name
		self.v = {} 
		self.fgroups={};
		self.vn = {}
		self.f={}
		self.VNIndex=0
		self.numberOfSkips=0	
		self.read_file(file_name)

		# return (self,.v, self.vn, self.f)

	def read_file(self, file_name):
	   	objFile = open(file_name, 'r')
	   	#if the parse function returns false we stop parsing
	   	#this is because we have to reach the faces
	   	for line in objFile:
		   	if not self.parse(line):
		   		break;

		#reparse to group into faces
		#generate_faces(self.f)
		for key in self.f.keys():
			face = self.f[key]
			lastfgroup=len(self.fgroups)
			lastf=len(self.fgroups[lastfgroup])
			if(face.v[2][2]-self.fgroups[lastfgroup][lastf].v[2][2]>0.01):
				self.fgroups[lastfgroup+1]={}
				self.fgroups[lastfgroup+1][1]=face
			else:
				self.fgroups[lastfgroup][lastf+1]=face

		index=0
		for fgroup in self.fgroups:
			index+=1
			write_file_from_f_group(fgroup,'file-layer'+str(index)+'.obj')


	
	def write_file_from_f_group(self,fgroup,output_file_name):
		outputFile = open(output_file_name, 'w')
		for i in fgroup.keys():
			for j in fgroup[i].v.keys():
				outStr = "v " + " ".join(str(x) for x in fgroup[i].v[j]) + "\n"
				outputFile.write(outStr)

		for i in fgroup.keys():
			for j in fgroup[i].vn.keys():
				outStr = "vn " + " ".join(str(x) for x in fgroup[i].vn[j]) + "\n"
				outputFile.write(outStr)

		for k in range(len(fgroup.keys())):
			outStr = "f " + str(3*k+1)+ "//" +  str(3*k+1) + " " + str(3*k+2) + "//" +  str(3*k+2) + " " + str(3*k+3) + "//" +  str(3*k+3) + "\n";
			outputFile.write(outStr)


	def write_file(self,output_file_name):
		outputFile = open(output_file_name, 'w')
		for key in self.v.keys():
			outStr = "v " + " ".join(str(x) for x in self.v[key]) + "\n"
			outputFile.write(outStr)

		for key in self.vn.keys():
			outStr = "vn " + " ".join(str(x) for x in self.vn[key]) + "\n"
			outputFile.write(outStr)

		#print all the numbers from 1 onwards
		for k in range(len(self.vn.keys())/3):
			outStr = "f " + str(3*k+1)+ "//" +  str(3*k+1) + " " + str(3*k+2) + "//" +  str(3*k+2) + " " + str(3*k+3) + "//" +  str(3*k+3) + "\n";
			outputFile.write(outStr)

	def generate_faces(self):
		#make faces available to memory
		vnkeys= self.vn.keys()
		for k in range(len(vnkeys)/3):
			vnkey=vnkeys[k]
			self.f[vnkey]={}
			self.f[vnkey].v=[]
			self.f[vnkey].v.append(self.v[k])
			self.f[vnkey].v.append(self.v[k+1])
			self.f[vnkey].v.append(self.v[k+2])
			self.f[vnkey].vn=[]
			self.f[vnkey].vn.append(self.vn[k])
			self.f[vnkey].vn.append(self.vn[k+1])
			self.f[vnkey].vn.append(self.vn[k+2])

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
		xyz = tuple(map(float, line.split()[1:]))
		#Using self.VNIndex so that we can delete the extra normals 
		self.VNIndex=self.VNIndex+1
		#If we have to skip this don't bother to check
		if self.numberOfSkips!=0:
			self.numberOfSkips-=1
		#Only keep faces where the y-vector normals < 20 radians
		#0.174533
		elif (self.angle_with_y(xyz) <= 0.174533*4):
			self.vn[self.VNIndex]=(xyz)
		else:
			self.numberOfSkips=(3-(self.VNIndex%3))%3
			
			##remove extra vn
			for i in range(0,3-self.numberOfSkips):
				self.vn.pop(self.VNIndex-i,None)	
			##remove extra v
			for i in range(self.numberOfSkips-2,self.numberOfSkips+1):
				self.v.pop(self.VNIndex+i,None)	

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

