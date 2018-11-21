import itertools
def next_bigger(n):
    for num in sorted([int(''.join(map(str,x))) for x in list(set(itertools.permutations([int(x) for x in str(n)])))]):
        if num>n:
            return num
    return -1