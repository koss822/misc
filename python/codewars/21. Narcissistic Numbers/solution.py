#!/usr/bin/env python3
def is_narcissistic(i):
    return sum(int(x)**(len(str(i))) for x in str(i)) == i
