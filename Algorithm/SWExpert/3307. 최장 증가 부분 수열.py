for t in range(int(input())):
    n = int(input())
    li = list(map(int, input().split()))
    cache = [1]*n
    for i in range(1, n):
        for j in range(i):
            if li[i] > li[j]:
                cache[i] = max(cache[i], cache[j]+1)
    print('#' + str(t+1), str(max(cache)))