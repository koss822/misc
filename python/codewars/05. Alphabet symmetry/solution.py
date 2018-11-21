def solve(arr):
    return list(map(lambda s: sum(1 if i+1==num else 0 for i,num in enumerate(list(map(lambda x: x-96, map(ord,s.lower()))))), arr))
print(solve(["IAMDEFANDJKL","thedefgh","xyzDEFghijabc"]))