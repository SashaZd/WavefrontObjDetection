

class ThreeDObject(object):
	
	"""docstring for Object"""

	def __init__(self,v,vn,f):
		self.v = v
		self.vn = vn
		self.f = vf

	def add_v(self,vertex):
		currentInd = len(self.v)+1
		self.v[currentInd] = vertex

	def add_vn(self,vertex_normal):
		currentInd = len(self.vn)+1
		self.vn[currentInd] = vertex_normal

	def add_face(self,face):
		currentInd=len(self.f)+1
		self.f[currentInd]=face
	
		