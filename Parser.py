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
		(x,y,z) = map(float, line.split()[1:])
		self.v[currentInd] = (x,y,z)

	def parse_vn(self, line):
		currentInd = len(self.vn)+1;
		(x,y,z) = map(float, line.split()[1:])
		self.vn[currentInd] = (x,y,z)

	def parse_f(self, line):
		currentInd = len(self.f)+1;
		(x, xn, y, yn, z, zn) = map(int, re.split(' |//',line)[1:])
		self.f[currentInd] = (x, xn, y, yn, z, zn)






		