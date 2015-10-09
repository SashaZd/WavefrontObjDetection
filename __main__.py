from Parser import Parser


file_name = 'Chair.obj.txt'
output_file_name = "FinalChair.obj.txt"


""" 
	Returns an object that contains 3 dictionaries: v, vn, f
	v[index] will give you the vertice coordinates at that index
	vn[index] will give you the vector normals (from origin) at that index
	f[index] will give you the face in the format (vx, vnx, vy, vny, vz, vnz) where f = vx//vnx vy//vny vz//vnz  
"""

outputFile = open(output_file_name, 'w')
parsedObj = Parser(file_name)
# print parsedObj.v[1]

for iv in range(1,len(parsedObj.v)):
	outStr = "v " + str(parsedObj.v[iv][0]) + " " +  str(parsedObj.v[iv][1]) + " " +  str(parsedObj.v[iv][2]) + "\n"
	outputFile.write(outStr)

for ivn in range(1,len(parsedObj.vn)):
	outStr = "vn " + str(parsedObj.vn[ivn][0]) + " " +  str(parsedObj.vn[ivn][1]) + " " +  str(parsedObj.vn[ivn][2]) + "\n"
	outputFile.write(outStr)

for key,value in parsedObj.f.items():
	outStr = "f " + str(value[0]) + "//" +  str(value[1]) + " " + str(value[2]) + "//" +  str(value[3]) + " " + str(value[4]) + "//" +  str(value[5]) + "\n";
	outputFile.write(outStr)

# for ifv in range(1,len(parsedObj.f)):
# 	outStr = "f " + str(parsedObj.f[ivn][0]) + "//" +  str(parsedObj.f[ivn][1]) + " " + str(parsedObj.f[ivn][2]) + "//" +  str(parsedObj.f[ivn][3]) + " " + str(parsedObj.f[ivn][4]) + "//" +  str(parsedObj.f[ivn][5]) + "\n";
# 	outputFile.write(outStr)

