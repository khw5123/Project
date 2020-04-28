a, b = map(int, input().strip().split(' '))
for i_ in range(b):
    for _ in range(a):
        print('*', end='')
    print()