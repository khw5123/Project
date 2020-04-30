def solve(master, rcs):
    save = []
    a, b, c, d, e, f = 0, 0, 0, 0, 0, 0
    for i in range(len(master)-1):
        a += master[i].count('(')
        b += master[i].count(')')
        c += master[i].count('{')
        d += master[i].count('}')
        e += master[i].count('[')
        f += master[i].count(']')
        dot = 0
        for j in range(len(master[i+1])-1):
            if master[i+1][j] == '.':
                dot += 1
            else:
                break
        save.append([a, b, c, d, e, f, dot])
    for i in range(1, 21):
        for j in range(1, 21):
            for k in range(1, 21):
                right = 0
                for l in range(len(save)):
                    if i*(save[l][0]-save[l][1]) + j*(save[l][2]-save[l][3]) + k*(save[l][4]-save[l][5]) == save[l][-1]:
                        right += 1
                if right == len(master)-1:
                    rcs.append([i, j, k])

for t in range(int(input())):
    p, q = map(int, input().split())
    master, me, rcs = [], [], []
    answer = []
    for _ in range(p):
        master.append(input())
    for _ in range(q):
        me.append(input())
    solve(master, rcs)
    if len(rcs) == 0:
        print('#' + str(t+1) + ' 0', end=' ')
        for _ in range(q-1):
            print(-1, end=' ')
        print()
    else:
        for i in range(len(rcs)):
            a, b, c, d, e, f = 0, 0, 0, 0, 0, 0
            answer.append([0])
            for j in range(len(me)-1):
                a += me[j].count('(')
                b += me[j].count(')')
                c += me[j].count('{')
                d += me[j].count('}')
                e += me[j].count('[')
                f += me[j].count(']')
                answer[-1].append(rcs[i][0]*(a-b) + rcs[i][1]*(c-d) + rcs[i][2]*(e-f))
        print('#' + str(t+1), end=' ')
        for i in range(len(answer[0])):
            confirm = True
            for j in range(len(answer)-1):
                if answer[j][i] != answer[j+1][i]:
                    confirm = False
                    break
            if confirm:
                print(answer[0][i], end=' ')
            else:
                print(-1, end=' ')
        print()