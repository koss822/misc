def find_sum(*numbers):
  return (-1 if min(numbers)<0 else sum(numbers)) if numbers else 0;
print(find_sum(1,2,3))
print(find_sum())
print(find_sum(-2,5))