for t in range(int(input())):
    n, m, k = map(int, input().split())
    li = sorted(list(map(int, input().split())))
    count = 0
    answer = True
    print('#' + str(t+1), end=' ')
    if li[0] == 0:
        print('Impossible')
    else:
        for i in range(1, li[-1]+1):
            if i % m == 0:
                count += k
            if li[0] == i:
                if count > 0:
                    count -= 1
                    del li[0]
                else:
                    answer = False
                    break
        if answer:
            print('Possible')
        else:
            print('Impossible')