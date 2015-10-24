

class ThreeDObject(object):
	
	"""ThreeDObject is a class for the wavefront representation of 3d objects"""

	def __init__(self,v,vn,):
		self.v = v
		self.vn = vn

	def add_v(self,vertex):
		currentInd = len(self.v)+1
		self.v[currentInd] = vertex

	def add_vn(self,vertex_normal):
		currentInd = len(self.vn)+1
		self.vn[currentInd] = vertex_normal

	
		