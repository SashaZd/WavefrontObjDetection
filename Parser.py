import time
import re
import numpy as np
import math
import operator
from collections import deque
from collections import defaultdict

OUTPUT_FILE_NAME = "CompressedRoomV1.obj"

class Parser(object):
	"""
		v1.1
		This defines a generalized parse dispatcher; 
		All parse functions reside in subclasses.
	"""


	def __init__(self, file_name,output_file,direction='y'):
		
		self.file_name = file_name
		self.output_file=output_file
		self.rounding_number = 1
		self.factor = 0.45
		if direction=='x':
			self.direction=0
		elif direction=='y':
			self.direction=1
		else:
			self.direction=2
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

		self.connected_components = []
		# self.visited_faces = {}

		print "Created parser object for file: ", self.file_name


	def readFile(self):
		objFile = open(self.file_name, 'r')

		line = objFile.readline()
		
		while(line[0:2] != "vn" and line[0:1] != "n"):
			if line[0:1] == "#":
				pass
			else:
				self.parse_v(line)

			line = objFile.readline()

		print "Starting with %d vertices & normals" % (len(self.v_queue))
		print time.time()
		# line currently contains the first vn line. 

		faceVns = (line, objFile.readline(), objFile.readline())
		
		while(faceVns[0][0:2] != "f "):
			flagVnSet = True

			for eachFace in faceVns: 
				xyz = tuple(map(float, eachFace.split()[1:]))
				square=xyz[0]*xyz[0] + xyz[1]* xyz[1]+ xyz[2]*xyz[2]
				# checking if Y-Normal is positive only. Need to add a min/max bound to this. 
				# if (self.angle_with_y(xyz) <= 0.174533*2):
				if -self.factor < (xyz[self.direction]) / square <self.factor:
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
		print time.time()

		self.v_list_unique_generator()

		print "Removing duplicates for connected components reduced to: %d vertices" % (len(self.v_list_unique))
		print time.time()



		# Temporary writing for connected components. Remove later.
		self.generate_v_with_face_indexes()

		

		print "After rounding off, we're left with %d vertices" % len(self.v_list_unique)
		print time.time()

		self.generate_connected_components()



	def generate_connected_components(self):
		print "Starting CC"
		print time.time()
		sorted_v_unique = sorted(self.v_list_unique.items(), key=operator.itemgetter(1))
		sorted_len=len(sorted_v_unique)
		cc2 = []
		#sreverse_list={}
		for i,v in enumerate(sorted_v_unique):
			v1= set(v[1])
			add_to_cc=True
			for j,t in enumerate(cc2):
				testSet=(t[1])
				if (testSet.intersection(v1)):
					cc2[j][0].append(v[0])
					cc2[j][1]=testSet.union(v1)
					add_to_cc=False
					break
			if(add_to_cc):
				cc2.append([[v[0]],v1])


			
		print "Done CC "
		outputFile = open(self.output_file, 'w')
		
		self.connected_components = cc2

		"""Prints connected components into individual object files"""
		self.write_connected_components_objFile()

	"""
		Used to print the connected components into individual object files
	"""
	def write_connected_components_objFile(self):
		
		OUTPUT_FILE_COMPLETE = self.output_file+'.obj'
		outputFile_complete = open(OUTPUT_FILE_COMPLETE, 'w')

		total_v = []
		count = 0

		print "Till here.... cc = ", len(self.connected_components)

		for index, (c, locs) in enumerate(self.connected_components): 
			if len(c) > 15:
				count = count + 1
				OUTPUT_FILE_NAME2="ConnectedComponent_%s.obj"% count
				outputFileTemp = open(OUTPUT_FILE_NAME2, 'w')
				v = []

				for eachFace in locs: 
					v.extend([((eachFace*3)-3), ((eachFace*3)-2), eachFace*3-1 ])

				total_v.extend(v)

				for eachV in v: 
					outputFileTemp.write(self.v_list[eachV])

				for eachV in v: 
					outputFileTemp.write(self.vn_list[eachV])

				for x in range(1,len(v),3):
					str_f = "f %d//%d %d//%d %d//%d \n" % (x, x, x+1, x+1, x+2, x+2)
					outputFileTemp.write(str_f)
			
			else:
				del self.connected_components[index]

		print "Now.... cc = ", len(self.connected_components), count


		for eachV in total_v:
			outputFile_complete.write(self.v_list[eachV])

		for eachV in total_v:
			outputFile_complete.write(self.vn_list[eachV])

		for x in range(1,len(total_v),3):
			str_f = "f %d//%d %d//%d %d//%d \n" % (x, x, x+1, x+1, x+2, x+2)
			outputFile_complete.write(str_f)



	def list_duplicates(self,seq):
		tally = defaultdict(list)
		for i,item in enumerate(seq):
			tally[item].append(i)
		return ((key,locs) for key,locs in tally.items() if len(locs)>1)


	# runs in a single pass and generates the defaultdict 
	def v_list_unique_generator(self):
		self.v_list_unique = defaultdict(list)
		seq = self.v_list
		for i,item in enumerate(seq):
			self.v_list_unique[item].append(i)

		# self.create_f_file()
				
	## To generate Temp_FV_CC.txt file with all unique vertices and the faces they belong to for merging.
	def generate_v_with_face_indexes(self):
		# sorted_v_unique = sorted(self.v_list_unique.items(), key=operator.itemgetter(1))
		v_with_indexes = {}
		

		""" Doesn't seem to be used
				v_new_list=[]
				for key in self.v_list:
					key_rounded = ([round(float(x),self.rounding_number) for x in key.split()[1:]])
					k = "v %f %f %f" % (key_rounded[0],key_rounded[1],key_rounded[2])
					v_new_list.append(k)
			
				self.write_f_file(v_new_list)
		"""

		for (key, indexes) in self.v_list_unique.items():
			key_rounded = tuple([round(float(x),self.rounding_number) for x in key.split()[1:]])
			indexes_faces = [x/3 for x in indexes]
			if key_rounded in v_with_indexes:
				v_with_indexes[key_rounded].extend(indexes_faces)
			else:
				v_with_indexes[key_rounded] = indexes_faces

		for (key, indexes) in v_with_indexes.items():
			v_with_indexes[key] = self.remove_list_duplicates(v_with_indexes[key])

		self.v_list_unique = v_with_indexes


	def write_f_file(self,v_list=[],vn_list=[]):
		outputFile = open(OUTPUT_FILE_NAME, 'w+')

		if(v_list==[]):
			v_list=self.v_list

		if(vn_list==[]):
			vn_list=self.vn_list

		for eachVertice in v_list:
			outputFile.write(eachVertice)
			outputFile.write("\n")

		for eachVerticeNormal in vn_list:
			outputFile.write(eachVerticeNormal)
			outputFile.write("\n")

		for x in xrange(1,len(self.v_list),3):
			f_str = "f %d//%d %d//%d %d//%d \n" % (x, x, x+1, x+1, x+2, x+2)
			outputFile.write(f_str)

	# Time 5 seconds
	def parse_v(self, line):
		self.v_queue.append(line)


	def parse_f(self, line):
		pass


	def remove_list_duplicates(self, seq):
		keys = {}
		for e in seq:
			keys[e] = 1
		return keys.keys()



