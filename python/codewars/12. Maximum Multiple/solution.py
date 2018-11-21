def max_multiple(divisor, bound):
    return max(x for x in range(0, bound+1) if x%divisor == 0)
print(max_multiple(5,23))