#!/usr/bin/env python3
def paint_letterboxes(start, finish):
    result = [0]*10
    for a in range(start,finish+1):
        for i in list(str(a)):
            result[int(i)]+=1
    return result
print(paint_letterboxes(125, 132))
#Test.assert_equals(paint_letterboxes(125, 132), [1,9,6,3,0,1,1,1,1,1])