#!/usr/bin/env python3
def sum_of_intervals(intervals):
    numbers = []
    for interval in intervals:
        for i in range(interval[0],interval[1]):
            numbers.append(i)
    return len(set(numbers))

print(sum_of_intervals( [
   [1,5],
   [1,5]
] ))
