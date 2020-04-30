for n in range(1, int(input())+1):
    count = 0
    for c in [c for c in str(n)]:
        if c in '369':
            count += 1
    if not count:
        print(n, end=' ')
    else:
        print('-' * count, end=' ')