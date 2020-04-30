for t in range(int(input())):
    n = int(input())
    answer = []
    li = []
    for _ in range(n):
        li.append(list(map(int, input().split())))
    for i in range(n):
        for j in range(n):
            if li[i][j] != 0:
                answer.append([])
                confirm = True
                for h in range(i+1, n):
                    if li[h][j] == 0:
                        answer[-1].append(h-i)
                        confirm = False
                        break
                if confirm:
                    answer[-1].append(n-i)
                confirm = True
                for w in range(j+1, n):
                    if li[i][w] == 0:
                        answer[-1].append(w-j)
                        confirm = False
                        break
                if confirm:
                    answer[-1].append(n-j)
                for h in range(i, i+answer[-1][0]):
                    for w in range(j, j+answer[-1][1]):
                        li[h][w] = 0
                answer[-1].insert(0, answer[-1][0]*answer[-1][1])
    answer.sort()
    print('#' + str(t+1), str(len(answer)), end=' ')
    for v in answer:
        print(v[1], v[2], end=' ')
    print()