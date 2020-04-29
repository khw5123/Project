def solve(i, j, k):
    result, idx = 0, 0
    for h in range(i-k+1, i+k):
        for w in range(j-idx, j+idx+1):
            if  0 <= h and h < n and 0 <= w and w < n:
                if li[h][w] == 1:
                    result += 1
        if h >= i:
            idx -= 1
        else:
            idx += 1
    return result

for t in range(int(input())):
    n, m = map(int, input().split())
    li = [list(map(int, input().split())) for _ in range(n)]
    total_count = 0
    for i in range(n):
        for j in range(n):
            if li[i][j] == 1:
                total_count += 1
    answer = 0
    for k in reversed(range(22)):
        cost = k*k + (k-1)*(k-1)
        if total_count*m - cost > 0:
            for i in range(n):
                for j in range(n):
                    count = solve(i, j, k)
                    if count*m - cost >= 0:
                        answer = max(answer, count)
    print('#' + str(t+1), str(answer))