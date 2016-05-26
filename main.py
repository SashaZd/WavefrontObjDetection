
import sys
import time
from Parser import Parser
from ConvexHulls import ConvexHulls

from shutil import copyfile

OBJ_FILE_NAME = sys.argv[-1]


# Start timer
t0 = time.time()
print "Starting at ", t0

"""
Reading the Object Room & Returning a Parser object
104 seconds
"""
directions=['z','y']
for direction in directions:
	parser = Parser(OBJ_FILE_NAME,OBJ_FILE_NAME+'_'+direction,direction)
	parser.readFile()

	#Stop timer
	t1 = time.time()
	total = t1-t0

	print total, " seconds to get connected components"
	print "Number of connected_components detected: ", len(parser.connected_components)

	count = 0
	for index, (c, locs) in enumerate(parser.connected_components): 
		if len(c) <= 20:
			del parser.connected_components[index]

	print "Count of files: ", count

	t2 = time.time()
	total = t2-t1
	print total, " seconds for this part"

	# """
	# Convex Polygons
	# """

	convexHull = ConvexHulls(parser.connected_components)

	t3 = time.time()
	total = t3-t2
	print total, " seconds for this part"

	print "Total Time: ", t3-t0

	# o_file_name = raw_input("Name this scene/mesh: ")

	o_file_name = "%s.txt" % (OBJ_FILE_NAME.split(".")[0])
	o_file = "../AR-SuperMarioBros-Backend/ARSuperMario/SurfaceDetectionOutput/%s" % (o_file_name)
	copyfile("Output_ConvexBoundaries.txt", o_file)

