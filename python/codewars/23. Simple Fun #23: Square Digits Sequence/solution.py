def mysquare(digits, previous = [], loop = 2):
    sum = 0
    for digit in str(digits):
        sum+=int(digit)**2
    if sum in previous or digits == sum:
        return loop
    else:
        previous.append(sum)
        return mysquare(sum, previous, loop+1)

def square_digits_sequence(n):
    return mysquare(n)

print(square_digits_sequence(545))