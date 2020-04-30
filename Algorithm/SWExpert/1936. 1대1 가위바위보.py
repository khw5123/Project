a, b = map(int, input().split())
if a - b == 1 or a - b == -2:
    print('A')
elif a - b == -1 or a - b == 2:
    print('B')