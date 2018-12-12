#!/usr/bin/env python3
def next_prime(n):
    while(True):
        n+=1
        if is_prime(n):
            return n

def is_prime(n):
    if n == 1:
        return False
    for i in range(2,n):
        if n%i==0:
            return False
    return True

print(next_prime(0))
print(next_prime(181))
print(next_prime(911))
