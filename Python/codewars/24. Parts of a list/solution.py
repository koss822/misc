#!/usr/bin/env python3
def partlist(arr):
    output = []
    for cycle in range(0, len(arr)-1):
        output.append((' '.join(arr[0:cycle+1]), ' '.join(arr[cycle+1:])))
    return output

print(partlist(["az", "toto", "picaro", "zone", "kiwi"]))
