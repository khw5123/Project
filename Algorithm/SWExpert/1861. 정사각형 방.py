def solve(x, y):
    ret = 1
    if y-1 >= 0 and li[y-1][x] == li[y][x]+1:
        ret += solve(x, y-1)
    elif y+1 < n and li[y+1][x] == li[y][x]+1:
        ret += solve(x, y+1)
    elif x-1 >= 0 and li[y][x-1] == li[y][x]+1:
        ret += solve(x-1, y)
    elif x+1 < n and li[y][x+1] == li[y][x]+1:
        ret += solve(x+1, y)
    return ret

for t in range(int(input())):
    n = int(input())
    answer = []
    li = []
    for _ in range(n):
        li.append(list(map(int, input().split())))
    for i in range(n):
        for j in range(n):
            answer.append([solve(j, i), li[i][j]])
    answer.sort(key=lambda x:(-x[0],x[1]))
    print('#' + str(t+1), str(answer[0][1]), str(answer[0][0]))