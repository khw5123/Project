for _ in range(10):
    t = int(input())
    n = list(map(int, input().split()))
    minus = 1
    while n[-1] > 0:
        n = n[1:len(n)] + [n[0]-minus]
        if minus == 5:
            minus = 1
        else:
            minus += 1
    n[-1] = 0
    print('#' + str(t), end=' ')
    for i in range(len(n)):
        print(n[i],end=' ')
    print()