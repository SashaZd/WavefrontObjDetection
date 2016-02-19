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

		self.connected_components = defaultdict(set)
		self.visited_faces = {}


	def readFile(self):
		objFile = open(self.file_name, 'r')

		line = objFile.readline()
		
		while(line[0:2] != "vn"):
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
		print time.time()

		self.v_list_unique_generator()

		print "Removing duplicates for connected components reduced to: %d vertices" % (len(self.v_list_unique))
		print time.time()

		# self.write_f_file()


		# Temporary writing for connected components. Remove later.
		# self.write_v_unique()

		self.generate_v_with_face_indexes()

		

		print "After rounding off, we're left with %d vertices" % len(self.v_list_unique)
		print time.time()

		self.generate_connected_components()



	def generate_connected_components(self):
		sorted_v_unique = sorted(self.v_list_unique.items(), key=operator.itemgetter(1))

		for (key, indexes) in sorted_v_unique:
			selected_component = -1
			visited_faces = sorted(list(set(indexes) & set(self.visited_faces)))

			# Found at least 1 visited face
			if len(visited_faces) > 0:

				# select the first component to merge the others into
				# Find
				selected_component = self.visited_faces[visited_faces.pop(0)]

				# Union
				for eachFace in visited_faces:

					# Merge other components
					checkComponent = self.visited_faces[eachFace]
					if checkComponent != selected_component:
						print "Merging Component: ", checkComponent, " with Component: ", selected_component
						# Make the visited component point to the new selected component
						for face in self.connected_components[checkComponent]:
							self.visited_faces[face]=selected_component

						# Merge both components into the one
						self.connected_components[selected_component].update(self.connected_components[checkComponent])
						self.connected_components[checkComponent] = set()

			# No faces were visited before. Adding new component
			else:
				selected_component = len(self.connected_components)
				# print "-------------- Creating Component: ", selected_component


			unvisited_faces = set(indexes) - set(visited_faces)
			for each in unvisited_faces:
				self.visited_faces[each] = selected_component

			self.connected_components[selected_component].update(unvisited_faces)

		outputFile = open("Temp_ConnectedComponents2", 'w')

		for (componentID, faces) in self.connected_components.items():
			out_str = "%s :: %d :: %s" % (componentID, len(faces), faces)
			outputFile.write(out_str)
			outputFile.write("\n")
			


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

		for (key, indexes) in self.v_list_unique.items():
			key_rounded = tuple([round(float(x),3) for x in key.split()[1:]])
			indexes_faces = [x/3 for x in indexes]
			if key_rounded in v_with_indexes:
				v_with_indexes[key_rounded].extend(indexes_faces)
			else:
				v_with_indexes[key_rounded] = indexes_faces

		for (key, indexes) in v_with_indexes.items():
			v_with_indexes[key] = self.remove_list_duplicates(v_with_indexes[key])

		# v_with_faces_sorted = sorted(v_with_indexes.items(), key=operator.itemgetter(1))
		# self.write_a_file_temp(v_with_faces_sorted)

		self.v_list_unique = v_with_indexes


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


	def remove_list_duplicates(self, seq):
		keys = {}
		for e in seq:
			keys[e] = 1
		return keys.keys()

	def write_a_file_temp(self, iterEle, file_name="Temp_FV_CC.txt"):
		# To see what the iterable looks like
		# Don't pass the iterable to this method to save time since this is for debug purposes only. 
		# Instead, just paste this into the calling method and delete later.

		outputFile = open(file_name, 'w')
		# outputFile.write(comment)

		# if isinstance(iterEle, dict):
		for (key, indexes) in iterEle:
			out_str = "%s :::: %s" % (key, indexes)
			outputFile.write(out_str)
			outputFile.write("\n")

		# elif isinstance(iterEle, list):
		# 	for element in iterEle:
		# 		# out_str = str(element)
		# 		outputFile.write(element)
		# 		outputFile.write("\n")

		# else:
		# 	pass


		


# Unused, check with Carl
	def angle_with_y(self,v1):
		"""Dot product, then normalize, then offset from origin"""
		v2=[0,1,0]
		
		cosang = np.dot(v1, v2)
		sinang = np.linalg.norm(np.cross(v1, v2))
		return np.arctan2(sinang, cosang)



