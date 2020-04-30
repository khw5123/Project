for t in range(int(input())):
    n = int(input())
    num = list(map(int, input().split()))
    answer, count = 0, 0
    for v in list(set(num)):
        if num.count(v) > count:
            count = num.count(v)
            answer = v
    print('#' + str(t+1) + ' ' + str(answer))