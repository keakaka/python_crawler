# Map
it = map(lambda x: print(x, end=' '), [1, 2, 3, 4])
next(it)
next(it)
next(it)
next(it)
print('\n=================================')

print(list(map(lambda x: x**2, [1, 2, 3, 4])))
print('=================================')

list(map(lambda x: print(x, end=' '), [1, 2, 3, 4]))

print('\n')
# Filter
lst = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
print(lst)
