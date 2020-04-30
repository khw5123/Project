def solve(w, b, r, li):
    result = 0
    state = ['W']*w + ['B']*b + ['R']*r
    for i in range(len(li)):
        for j in range(len(li[0])):
            if li[i][j] != state[i]:
                result += 1
    return result

for t in range(int(input())):
    n, m = map(int, input().split())
    li = [list(map(str, input())) for _ in range(n)]
    answer = 2501
    for i in range(1, n):
        for j in range(1, n):
            if n-(i+j) > 0:
                answer = min(answer, solve(i, j, n-(i+j), li))
    print('#' + str(t+1), str(answer))