import time
from Parser import Parser

# Start timer
t0 = time.time()
print "Starting...."

print t0 
parser = Parser("FullRoom.obj.txt")
parser.readFile()



#Stop timer
t1 = time.time()
total = t1-t0

print total, " seconds"
