for t in range(int(input())):
    a, b = map(str, input().split())
    cache = [[0]*1001 for i in range(1001)]
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                cache[i][j] = cache[i-1][j-1]+1
            else:
                cache[i][j] = max(cache[i-1][j], cache[i][j-1])
    print('#' + str(t+1), str(cache[len(a)][len(b)]))