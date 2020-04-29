for t in range(int(input())):
    n, m, k = map(int, input().split())
    li = [list(map(int, input().split())) for _ in range(n)]
    answer = 0
    cell = dict()
    for i in range(n):
        for j in range(m):
            if li[i][j] != 0:
                cell[(i, j)] = [li[i][j], li[i][j]]
    for _ in range(k):
        create = dict()
        for k, v in cell.items():
            if v[0] == 0:
                if (k[0]-1, k[1]) not in cell:
                    if (k[0]-1, k[1]) in create:
                        if v[1] > create[(k[0]-1, k[1])][1]:
                            create[(k[0]-1, k[1])][1] = [v[1], v[1]]
                    else:
                        create[(k[0]-1, k[1])] = [v[1], v[1]]
                if (k[0]+1, k[1]) not in cell:
                    if (k[0]+1, k[1]) in create:
                        if v[1] > create[(k[0]+1, k[1])][1]:
                            create[(k[0]+1, k[1])][1] = [v[1], v[1]]
                    else:
                        create[(k[0]+1, k[1])] = [v[1], v[1]]
                if (k[0], k[1]-1) not in cell:
                    if (k[0], k[1]-1) in create:
                        if v[1] > create[(k[0], k[1]-1)][1]:
                            create[(k[0], k[1]-1)][1] = [v[1], v[1]]
                    else:
                        create[(k[0], k[1]-1)] = [v[1], v[1]]
                if (k[0], k[1]+1) not in cell:
                    if (k[0], k[1]+1) in create:
                        if v[1] > create[(k[0], k[1]+1)][1]:
                            create[(k[0], k[1]+1)][1] = [v[1], v[1]]
                    else:
                        create[(k[0], k[1]+1)] = [v[1], v[1]]
            cell[k][0] -= 1
        for k, v in create.items():
            cell[k] = v
    for k, v in cell.items():
        if v[0] > -v[1]:
            answer += 1
    print('#' + str(t+1), str(answer))