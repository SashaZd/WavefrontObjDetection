from Parser import Parser


file_name = 'Chair.obj'
output_file_name = "FinalChair2.obj"


""" 
	Returns an object that contains 3 dictionaries: v, vn, f
	v[index] will give you the vertice coordinates at that index
	vn[index] will give you the vector normals (from origin) at that index
	f[index] will give you the face in the format (vx, vnx, vy, vny, vz, vnz) where f = vx//vnx vy//vny vz//vnz  
"""

#outputFile = open(output_file_name, 'w')
parsedObj = Parser(file_name)
# print parsedObj.v[1]
parsedObj.write_file(output_file_name)
