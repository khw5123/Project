for t in range(int(input())):
    m, bc = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    li = [[[0]]*10 for _ in range(10)]
    answer = 0
    for k in range(bc):
        x, y, c, p = map(int, input().split())
        x, y = x-1, y-1
        idx = 0
        for i in range(y-c, y-c+2*c+1):
            for j in range(x-idx, x-idx+2*idx+1):
                if 0 <= i and i < 10 and 0 <= j and j < 10:
                    if li[i][j][0] == 0:
                        li[i][j] = [[k+1, p]]
                    else:
                        li[i][j].append([k+1, p])
                        li[i][j].sort(key=lambda x:x[1])
            if i <= y:
                if i == y:
                    idx -= 1
                else:
                    idx += 1
            else:
                idx -= 1   
    pos_a, pos_b = [0, 0], [9, 9]
    for i in range(-1, m):
        if i != -1:
            if a[i] == 1:
                pos_a = [pos_a[0]-1, pos_a[1]]
            elif a[i] == 2:
                pos_a = [pos_a[0], pos_a[1]+1]
            elif a[i] == 3:
                pos_a = [pos_a[0]+1, pos_a[1]]
            elif a[i] == 4:
                pos_a = [pos_a[0], pos_a[1]-1]
            if b[i] == 1:
                pos_b = [pos_b[0]-1, pos_b[1]]
            elif b[i] == 2:
                pos_b = [pos_b[0], pos_b[1]+1]
            elif b[i] == 3:
                pos_b = [pos_b[0]+1, pos_b[1]]
            elif b[i] == 4:
                pos_b = [pos_b[0], pos_b[1]-1]
        if type(li[pos_a[0]][pos_a[1]][0]) == list and type(li[pos_b[0]][pos_b[1]][0]) == list:
            if len(li[pos_a[0]][pos_a[1]]) == 1 and len(li[pos_b[0]][pos_b[1]]) == 1:
                if li[pos_a[0]][pos_a[1]] == li[pos_b[0]][pos_b[1]]:
                    answer += li[pos_a[0]][pos_a[1]][-1][1]
                else:
                    answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_b[0]][pos_b[1]][-1][1])
            else:
                if len(li[pos_a[0]][pos_a[1]]) == 1 and len(li[pos_b[0]][pos_b[1]]) != 1:
                    if li[pos_a[0]][pos_a[1]][-1] == li[pos_b[0]][pos_b[1]][-1]:
                        answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_b[0]][pos_b[1]][-2][1])
                    else:
                        answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_b[0]][pos_b[1]][-1][1])
                elif len(li[pos_a[0]][pos_a[1]]) != 1 and len(li[pos_b[0]][pos_b[1]]) == 1:
                    if li[pos_a[0]][pos_a[1]][-1] == li[pos_b[0]][pos_b[1]][-1]:
                        answer += (li[pos_b[0]][pos_b[1]][-1][1] + li[pos_a[0]][pos_a[1]][-2][1])
                    else:
                        answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_b[0]][pos_b[1]][-1][1])
                else:
                    if li[pos_a[0]][pos_a[1]][-1] == li[pos_b[0]][pos_b[1]][-1]:
                        if li[pos_a[0]][pos_a[1]][-2][1] > li[pos_b[0]][pos_b[1]][-2][1]:
                            answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_a[0]][pos_a[1]][-2][1])
                        else:
                            answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_b[0]][pos_b[1]][-2][1])
                    else:
                        answer += (li[pos_a[0]][pos_a[1]][-1][1] + li[pos_b[0]][pos_b[1]][-1][1])
        elif type(li[pos_a[0]][pos_a[1]][0]) == list and type(li[pos_b[0]][pos_b[1]][0]) != list:
            answer += li[pos_a[0]][pos_a[1]][-1][1]
        elif type(li[pos_a[0]][pos_a[1]][0]) != list and type(li[pos_b[0]][pos_b[1]][0]) == list:
            answer += li[pos_b[0]][pos_b[1]][-1][1]
    print('#' + str(t+1), str(answer))