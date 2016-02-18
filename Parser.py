import time
import re
import numpy as np
import math
from collections import deque
from collections import defaultdict

OUTPUT_FILE_NAME = "CompressedRoomV1.obj"

class Parser(object):
	"""
		v1.0
		This defines a generalized parse dispatcher; 
		All parse functions reside in subclasses.
	"""


	def __init__(self, file_name):
		
		self.file_name = file_name

		"""
		v1.0.1
		Reading file just once. All vertices are read into a queue. On the basis of a trio of normals (per face), 
		If all -0.3 >=normal >=03:
			corresponded vertices are popped into final vertice v_list
			normals are added into final normal vn_list
		Else: 
			discarded 
		"""
		self.v_queue = deque([])
		self.v_list = []
		self.vn_list = []
		

		self.v_list_unique = defaultdict(list)


	def readFile(self):
		objFile = open(self.file_name, 'r')

		line = objFile.readline()
		
		while(line[0:2] != "vn"):
			if line[0:1] == "#":
				pass
			else:
				self.parse_v(line)
			line = objFile.readline()

		# line currently contains the first vn line. 

		faceVns = (line, objFile.readline(), objFile.readline())
		
		while(faceVns[0][0:2] != "f "):
			flagVnSet = True
			for eachFace in faceVns: 
				xyz = tuple(map(float, eachFace.split()[1:]))
				
				# checking if Y-Normal is positive only. Need to add a min/max bound to this. 
				# if (self.angle_with_y(xyz) <= 0.174533*2):
				if -0.17 < xyz[1] < 0.17:
					flagVnSet = False
			
			if flagVnSet == True:
				self.vn_list.extend(faceVns)
				self.v_list.extend((self.v_queue.popleft(), self.v_queue.popleft(), self.v_queue.popleft()))

			else:	
				self.v_queue.popleft()
				self.v_queue.popleft()
				self.v_queue.popleft()

			faceVns = (objFile.readline(), objFile.readline(), objFile.readline())

		# Time till here 42  seconds
		# Number of V&Vns : 8595078 (each)

		print "Reduced to %d vertices & %d normals" % (len(self.v_list), len(self.vn_list))

		self.v_list_unique_generator()

		print "Removing duplicates for connected components reduced to: %d vertices" % (len(self.v_list_unique))

		# self.write_f_file()

		# Temporary writing for connected components. Remove later.
		self.write_v_unique()


	# runs in a single pass and generates the defaultdict 
	def v_list_unique_generator(self):
		tally = defaultdict(list)
		seq = self.v_list
		for i,item in enumerate(seq):
			tally[item].append(i)
		
		self.v_list_unique = tally #((key,locs) for key,locs in tally.items() if len(locs)>1)


		# self.create_f_file()
					
	def write_f_file(self):
		outputFile = open(OUTPUT_FILE_NAME, 'w')

		for eachVertice in self.v_list:
			outputFile.write(eachVertice)
			outputFile.write("\n")

		for eachVerticeNormal in self.vn_list:
			outputFile.write(eachVerticeNormal)
			outputFile.write("\n")

		for x in xrange(1,len(self.v_list),3):
			f_str = "f %d//%d %d//%d %d//%d \n" % (x, x, x+1, x+1, x+2, x+2)
			outputFile.write(f_str)

	def write_v_unique(self):
		outputFile = open("Temp_V_Unique.txt", 'w')

		for (key, indexes) in self.v_list_unique.items():
			out_str = "( %s ) : %s" % (key[:-2], indexes)
			outputFile.write(out_str)
			outputFile.write("\n")
		

	# Time 5 seconds
	def parse_v(self, line):
		self.v_queue.append(line)


	def parse_vn(self, line):
		pass
		# xyz = tuple(map(float, line.split()[1:]))

		# #Only keep faces where qthe y-vector normals < 20 radians
		# #0.174533

		# # if (self.angle_with_y(xyz) <= 0.174533*2):
		# if xyz[1] > 0:
		# 	self.vn_queue.append(xyz)
		# else:
		# 	pass		

	def parse_f(self, line):
		pass


# Unused, check with Carl
	def angle_with_y(self,v1):
		"""Dot product, then normalize, then offset from origin"""
		v2=[0,1,0]
		
		cosang = np.dot(v1, v2)
		sinang = np.linalg.norm(np.cross(v1, v2))
		return np.arctan2(sinang, cosang)



