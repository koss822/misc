import numpy
def spinning_rings(inner_max, outer_max):
   i = 0
   inner = numpy.arange(0,inner_max+1)[::-1]
   outer = numpy.arange(0,outer_max+1)
   while True:
     if numpy.roll(inner,-i)[0] == numpy.roll(outer,-i-1)[0]:
       return i+1
     i += 1
print(spinning_rings(3, 3))