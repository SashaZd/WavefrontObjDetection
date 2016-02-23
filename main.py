import time
from Parser import Parser

# Start timer
t0 = time.time()
print "Starting at ", t0

parser = Parser("FullRoom.obj")
parser.readFile()

#Stop timer
t1 = time.time()
total = t1-t0

print total, " seconds to get connected components"

print "Number of connected_components detected: ", len(parser.connected_components)
