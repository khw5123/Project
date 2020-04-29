import copy
import itertools

def solve(a, b):
    result = 0
    while True:
        result += 1
        queue_a, queue_b = 0, 0
        confirm_a, confirm_b = True, True
        a.sort()
        b.sort()
        for i in range(len(a)):
            if a[i] == 0:
                if queue_a < 3:
                    a[i] -= 1
            else:
                a[i] -= 1
            if a[i] < 0 and a[i] > -li[stair_a[0]][stair_a[1]]-1:
                queue_a += 1
            if a[i] > -li[stair_a[0]][stair_a[1]]-1:
                confirm_a = False
        for i in range(len(b)):
            if b[i] == 0:
                if queue_b < 3:
                    b[i] -= 1
            else:
                b[i] -= 1
            if b[i] < 0 and b[i] > -li[stair_b[0]][stair_b[1]]-1:
                queue_b += 1
            if b[i] > -li[stair_b[0]][stair_b[1]]-1:
                confirm_b = False
        if confirm_a and confirm_b:
            break
    return result

for t in range(int(input())):
    n = int(input())
    li = [list(map(int, input().split())) for _ in range(n)]
    stair_a, stair_b, ab = [], [], []
    answer = 987654321
    for i in range(n):
        for j in range(n):
            if li[i][j] != 0 and li[i][j] != 1:
                if len(stair_a) == 0:
                    stair_a = [i, j]
                else:
                    stair_b = [i, j]
            elif li[i][j] == 1:
                ab.append([i, j])
    for k in range(len(ab)+1):
        tmp = list(itertools.combinations(ab, k))
        for i in range(len(tmp)):
            tmp_a, tmp_b = list(copy.deepcopy(tmp[i])), []
            for j in range(len(ab)):
                if ab[j] not in tmp_a:
                    tmp_b.append(ab[j])
            a, b = [], []
            for j in range(len(tmp_a)):
                a.append(abs(tmp_a[j][0] - stair_a[0]) + abs(tmp_a[j][1] - stair_a[1]))
            for j in range(len(tmp_b)):
                b.append(abs(tmp_b[j][0] - stair_b[0]) + abs(tmp_b[j][1] - stair_b[1]))
            answer = min(answer, solve(a, b))
    print('#' + str(t+1), str(answer))