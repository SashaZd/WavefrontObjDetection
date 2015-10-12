import re

class Parser(object):
	"""
		This defines a generalized parse dispatcher; 
		All parse functions reside in subclasses.

		NOTE: New optimization. Since MS Kinect creates a new face for each vertex,
		and does not reuse vertices, we can avoid reading the part of the file that 
		contains information about the faces
		Time before optimization: 4min approx
		Time after  optimization: 3min approx

		File size decrease by deleting normals 
	"""

	def __init__(self, file_name):
		self.file_name = file_name
		self.v = {}
		self.vn = {}
		self.f = {}
		self.VNIndex=0
		self.read_file(file_name)

		# return (self.v, self.vn, self.f)

	def read_file(self, file_name):
	   	objFile = open(file_name, 'r')
	   	#if the parse function returns false we stop parsing
	   	#this is because we have to reach the faces
	   	for line in objFile:
		   	if not self.parse(line):
		   		break;

	def write_file(self,output_file_name):
		outputFile = open(output_file_name, 'w')
		for key in self.v.keys():
			outStr = "v " + " ".join(str(x) for x in self.v[key]) + "\n"
			outputFile.write(outStr)

		for key in self.vn.keys():
			outStr = "vn " + " ".join(str(x) for x in self.vn[key]) + "\n"
			outputFile.write(outStr)

		vnkeys=self.vn.keys()
		for k in range(len(vnkeys)/3):
			outStr = "f " + str(vnkeys[k]) + "//" +  str(vnkeys[k]) + " " + str(vnkeys[k+1]) + "//" +  str(vnkeys[k+1]) + " " + str(vnkeys[k+2]) + "//" +  str(vnkeys[k+2]) + "\n";
			outputFile.write(outStr)

	def parse(self, line):
	   	"""Determine what type of line we are and dispatch appropriately."""
	   
   		if line[0:2] == "#":
			pass;

		elif line[0:2] == "v ":
			self.parse_v(line)

		elif line[0:2] == "vn":
			self.parse_vn(line)

		elif line[0:2] == "f ":
			#self.parse_f(line)
			return False

		return True

	def parse_v(self, line):
		currentInd=len(self.v)+1
		xyz = tuple(map(float, line.split()[1:]))
		self.v[currentInd]=xyz


	def parse_vn(self, line):
		xyz = tuple(map(float, line.split()[1:]))
		self.VNIndex=self.VNIndex+1
		#Only keep faces where the y-vector normals >= 0
		if (xyz[1] >= 0):
			self.vn[self.VNIndex]=(xyz)
		else:
			self.v.pop(self.VNIndex)

	def parse_f(self, line):
		"""
			Only keep faces where the y-vector normals >= 0
			Reduced number of faces from 613498 to 379666
		"""

		currentInd = len(self.f)+1

		# (x, xn, y, yn, z, zn) <-- format
		checkFace = map(int, re.split(' |//',line)[1:])

		# Check values for y normals to ensure all are positive
		# otherwise delete those extra normals and vertices that are present
		ynormals = [self.vn[checkFace[1]][1], self.vn[checkFace[3]][1], self.vn[checkFace[5]][1]]
		if all(vny >= 0 for vny in ynormals):
			self.f[currentInd] = tuple(checkFace)
		else:
			del self.vn[checkFace[1]]
			del self.vn[checkFace[3]]
			del self.vn[checkFace[5]]
			del self.v[checkFace[0]]
			del self.v[checkFace[2]]
			del self.v[checkFace[4]]
