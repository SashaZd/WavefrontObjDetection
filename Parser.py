import re

class Parser(object):
	"""
		This defines a generalized parse dispatcher; 
		All parse functions reside in subclasses.
	"""

	def __init__(self, file_name):
		self.file_name = file_name
		self.v = {}
		self.vn = {}
		self.f = {}
		self.read_file(file_name)

		# return (self.v, self.vn, self.f)

	def read_file(self, file_name):
	   	objFile = open(file_name, 'r')
	   	for line in objFile:
		   	self.parse(line)

	def parse(self, line):
	   	"""Determine what type of line we are and dispatch appropriately."""
	   
   		if line[0:2] == "#":
			pass;

		elif line[0:2] == "v ":
			self.parse_v(line)

		elif line[0:2] == "vn":
			self.parse_vn(line)

		elif line[0:2] == "f ":
			self.parse_f(line)

	def parse_v(self, line):
		currentInd = len(self.v)+1
		xyz = tuple(map(float, line.split()[1:]))
		self.v[currentInd] = xyz

	def parse_vn(self, line):
		currentInd = len(self.vn)+1;
		xyz = tuple(map(float, line.split()[1:]))
		self.vn[currentInd] = xyz

	def parse_f(self, line):
		"""
			Only keep faces where the y-vector normals >= 0
			Reduced number of faces from 613498 to 379666
		"""

		currentInd = len(self.f)+1

		# (x, xn, y, yn, z, zn) <-- format
		checkFace = map(int, re.split(' |//',line)[1:])

		# Check values for y normals to ensure all are positive
		
		ynormals = [self.vn[checkFace[1]][1], self.vn[checkFace[3]][1], self.vn[checkFace[5]][1]]
		if all(vny >= 0 for vny in ynormals):
			self.f[currentInd] = tuple(checkFace)

		






		