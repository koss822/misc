def high_and_low(numbers):
    arr = [int(i) for i in numbers.split(' ')]
    return " ".join([str(max(arr)), str(min(arr))])