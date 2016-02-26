import time
from Parser import Parser
from ConvexHulls import ConvexHulls

# Start timer
t0 = time.time()
print "Starting at ", t0

"""
Reading the Object Room & Returning a Parser object
104 seconds
"""

# parser = Parser("FullRoom.obj")
# parser.readFile()

# #Stop timer
# t1 = time.time()
# total = t1-t0

# print total, " seconds to get connected components"
# print "Number of connected_components detected: ", len(parser.connected_components)

# count = 0
# for index, (c, locs) in enumerate(parser.connected_components): 
# 	if len(c) <= 15:
# 		del parser.connected_components[index]

# print "Count of files: ", count


# """
# Convex Polygons
# """

# convexHull = ConvexHulls(parser.connected_components)

convexHull = ConvexHulls()

