test = {1:[1], 2:[2, 4, 8, 6], 3:[3, 9, 7, 1], 4:[4, 6], 5:[5], 6:[6], 7:[7, 9, 3, 1], 8:[8, 4, 2, 6], 9:[9, 1]}

count = int(input(''))
for _ in range(count):
    a, b = map(int, input().split())
    if a % 10 == 0:
        print(10)
    else:
        print(test[int(str(a)[-1])][b % len(test[int(str(a)[-1])]) - 1])