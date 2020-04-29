import itertools

def check(li):
    if k != 1:
        for j in range(w):
            confirm, count = False, 1
            for i in range(d-1):
                if li[i][j] == li[i+1][j]:
                    count += 1
                else:
                    count = 1
                if count == k:
                    confirm = True
                    break
            if not confirm:
                return False
    return True

def solve(change):
    for i in range(len(change)):
        for j in range(pow(2, len(change[i]))):
            n = '0'*(len(change[i]) - len(bin(j)[2:])) + bin(j)[2:]
            if change[i][0] == 0:
                tmp = []
            else:
                tmp = li[:change[i][0]]
            for l in range(len(change[i])):
                if n[l] == '0':
                    tmp += [[0]*w]
                else:
                    tmp += [[1]*w]
                if l == len(change[i])-1:
                    if change[i][l] != d-1:
                        tmp += li[change[i][l]+1:]
                else:
                    tmp += li[change[i][l]+1:change[i][l+1]]
            if check(tmp):
                return True
    return False

for t in range(int(input())):
    d, w, k = map(int, input().split())
    li = [list(map(int, input().split())) for _ in range(d)]
    answer = 0
    if not check(li):
        for i in range(1, d+1):
            change = list(itertools.combinations([j for j in range(d)], i))
            if solve(change):
                answer = i
                break
    print('#' + str(t+1), str(answer))