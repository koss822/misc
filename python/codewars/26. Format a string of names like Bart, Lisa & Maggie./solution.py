#!/usr/bin/env python3
def namelist(names):
    mynames = [list(name.values())[0] for name in names]
    output = mynames[:-2]
    output.append(" & ".join(mynames[-2:]))
    return ", ".join(output)

print(namelist([{'name': 'Bart'},{'name': 'Lisa'},{'name': 'Maggie'},{'name': 'Homer'},{'name': 'Marge'}]))
