def is_zero_balanced(arr):
    return True if arr and sorted([x for x in arr if x>0]) == sorted(map(lambda x: x*-1, [x for x in arr if x<0])) and sum(arr)==0 else False