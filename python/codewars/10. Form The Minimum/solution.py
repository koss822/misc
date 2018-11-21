def min_value(digits):
 return int("".join([str(x) for x in sorted(set(digits))]))
print(min_value([4, 8, 1, 4]))