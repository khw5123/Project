for t in range(int(input())):
    s = input()
    print('#' + str(t+1), end=' ')
    for c in s:
        if c not in 'aeiou':
            print(c, end='')
    print()