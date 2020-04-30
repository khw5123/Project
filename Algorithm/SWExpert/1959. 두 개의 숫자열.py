for t in range(int(input())):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    answer = 0
    if n > m:
        for i in range(n-m+1):
            tmp = 0
            for j in range(m):
                tmp += (a[i+j] * b[j])
            answer = max(answer, tmp)
    else:
        for i in range(m-n+1):
            tmp = 0
            for j in range(n):
                tmp += (b[i+j] * a[j])
            answer = max(answer, tmp)
    print('#' + str(t+1) + ' ' + str(answer))