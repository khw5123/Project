import copy

def solve(pos, d):
    start = copy.deepcopy(pos)
    score = 0
    while True:
        if d == 'u':
            if pos[0]-1 == -1:
                score += 1
                if li[pos[0]][pos[1]] == 1:
                    score += 1
                    d = 'r'
                elif li[pos[0]][pos[1]] == 4:
                    score += 1
                    d = 'l'
                elif li[pos[0]][pos[1]] == 6 or li[pos[0]][pos[1]] == 7 or li[pos[0]][pos[1]] == 8 or li[pos[0]][pos[1]] == 9 or li[pos[0]][pos[1]] == 10:
                    for l in di[li[pos[0]][pos[1]]]:
                        if l != pos:
                            pos = l
                            d = 'd'
                            break
                elif pos == start:
                    break
                else:
                    d = 'd'
            elif li[pos[0]-1][pos[1]] == 1:
                score += 1
                d = 'd'
                pos = [pos[0]-1, pos[1]]
            elif li[pos[0]-1][pos[1]] == 2:
                score += 1
                d = 'r'
                pos = [pos[0]-1, pos[1]]
            elif li[pos[0]-1][pos[1]] == 3:
                score += 1
                d = 'l'
                pos = [pos[0]-1, pos[1]]
            elif li[pos[0]-1][pos[1]] == 4:
                score += 1
                d = 'd'
                pos = [pos[0]-1, pos[1]]
            elif li[pos[0]-1][pos[1]] == 5:
                score += 1
                d = 'd'
                pos = [pos[0]-1, pos[1]]
            elif li[pos[0]-1][pos[1]] == 6 or li[pos[0]-1][pos[1]] == 7 or li[pos[0]-1][pos[1]] == 8 or li[pos[0]-1][pos[1]] == 9 or li[pos[0]-1][pos[1]] == 10:
                for l in di[li[pos[0]-1][pos[1]]]:
                    if l != [pos[0]-1, pos[1]]:
                        pos = l
                        break
            elif li[pos[0]-1][pos[1]] == -1:
                break
            elif [pos[0]-1, pos[1]] == start:
                break
            else:
                pos = [pos[0]-1, pos[1]]
        elif d == 'd':
            if pos[0]+1 == n:
                score += 1
                if li[pos[0]][pos[1]] == 2:
                    score += 1
                    d = 'r'
                elif li[pos[0]][pos[1]] == 3:
                    score += 1
                    d = 'l'
                elif li[pos[0]][pos[1]] == 6 or li[pos[0]][pos[1]] == 7 or li[pos[0]][pos[1]] == 8 or li[pos[0]][pos[1]] == 9 or li[pos[0]][pos[1]] == 10:
                    for l in di[li[pos[0]][pos[1]]]:
                        if l != pos:
                            pos = l
                            d = 'u'
                            break
                elif pos == start:
                    break
                else:
                    d = 'u'
            elif li[pos[0]+1][pos[1]] == 1:
                score += 1
                d = 'r'
                pos = [pos[0]+1, pos[1]]
            elif li[pos[0]+1][pos[1]] == 2:
                score += 1
                d = 'u'
                pos = [pos[0]+1, pos[1]]
            elif li[pos[0]+1][pos[1]] == 3:
                score += 1
                d = 'u'
                pos = [pos[0]+1, pos[1]]
            elif li[pos[0]+1][pos[1]] == 4:
                score += 1
                d = 'l'
                pos = [pos[0]+1, pos[1]]
            elif li[pos[0]+1][pos[1]] == 5:
                score += 1
                d = 'u'
                pos = [pos[0]+1, pos[1]]
            elif li[pos[0]+1][pos[1]] == 6 or li[pos[0]+1][pos[1]] == 7 or li[pos[0]+1][pos[1]] == 8 or li[pos[0]+1][pos[1]] == 9 or li[pos[0]+1][pos[1]] == 10:
                for l in di[li[pos[0]+1][pos[1]]]:
                    if l != [pos[0]+1, pos[1]]:
                        pos = l
                        break
            elif li[pos[0]+1][pos[1]] == -1:
                break
            elif [pos[0]+1, pos[1]] == start:
                break
            else:
                pos = [pos[0]+1, pos[1]]
        elif d == 'l':
            if pos[1]-1 == -1:
                score += 1
                if li[pos[0]][pos[1]] == 3:
                    score += 1
                    d = 'd'
                elif li[pos[0]][pos[1]] == 4:
                    score += 1
                    d = 'u'
                elif li[pos[0]][pos[1]] == 6 or li[pos[0]][pos[1]] == 7 or li[pos[0]][pos[1]] == 8 or li[pos[0]][pos[1]] == 9 or li[pos[0]][pos[1]] == 10:
                    for l in di[li[pos[0]][pos[1]]]:
                        if l != pos:
                            pos = l
                            d = 'r'
                            break
                elif pos == start:
                    break
                else:
                    d = 'r'
            elif li[pos[0]][pos[1]-1] == 1:
                score += 1
                d = 'u'
                pos = [pos[0], pos[1]-1]
            elif li[pos[0]][pos[1]-1] == 2:
                score += 1
                d = 'd'
                pos = [pos[0], pos[1]-1]
            elif li[pos[0]][pos[1]-1] == 3:
                score += 1
                d = 'r'
                pos = [pos[0], pos[1]-1]
            elif li[pos[0]][pos[1]-1] == 4:
                score += 1
                d = 'r'
                pos = [pos[0], pos[1]-1]
            elif li[pos[0]][pos[1]-1] == 5:
                score += 1
                d = 'r'
                pos = [pos[0], pos[1]-1]
            elif li[pos[0]][pos[1]-1] == 6 or li[pos[0]][pos[1]-1] == 7 or li[pos[0]][pos[1]-1] == 8 or li[pos[0]][pos[1]-1] == 9 or li[pos[0]][pos[1]-1] == 10:
                for l in di[li[pos[0]][pos[1]-1]]:
                    if l != [pos[0], pos[1]-1]:
                        pos = l
                        break
            elif li[pos[0]][pos[1]-1] == -1:
                break
            elif [pos[0], pos[1]-1] == start:
                break
            else:
                pos = [pos[0], pos[1]-1]
        elif d == 'r':
            if pos[1]+1 == n:
                score += 1
                if li[pos[0]][pos[1]] == 1:
                    score += 1
                    d = 'u'
                elif li[pos[0]][pos[1]] == 2:
                    score += 1
                    d = 'd'
                elif li[pos[0]][pos[1]] == 6 or li[pos[0]][pos[1]] == 7 or li[pos[0]][pos[1]] == 8 or li[pos[0]][pos[1]] == 9 or li[pos[0]][pos[1]] == 10:
                    for l in di[li[pos[0]][pos[1]]]:
                        if l != pos:
                            pos = l
                            d = 'l'
                            break
                elif pos == start:
                    break
                else:
                    d = 'l'
            elif li[pos[0]][pos[1]+1] == 1:
                score += 1
                d = 'l'
                pos = [pos[0], pos[1]+1]
            elif li[pos[0]][pos[1]+1] == 2:
                score += 1
                d = 'l'
                pos = [pos[0], pos[1]+1]
            elif li[pos[0]][pos[1]+1] == 3:
                score += 1
                d = 'd'
                pos = [pos[0], pos[1]+1]
            elif li[pos[0]][pos[1]+1] == 4:
                score += 1
                d = 'u'
                pos = [pos[0], pos[1]+1]
            elif li[pos[0]][pos[1]+1] == 5:
                score += 1
                d = 'l'
                pos = [pos[0], pos[1]+1]
            elif li[pos[0]][pos[1]+1] == 6 or li[pos[0]][pos[1]+1] == 7 or li[pos[0]][pos[1]+1] == 8 or li[pos[0]][pos[1]+1] == 9 or li[pos[0]][pos[1]+1] == 10:
                for l in di[li[pos[0]][pos[1]+1]]:
                    if l != [pos[0], pos[1]+1]:
                        pos = l
                        break
            elif li[pos[0]][pos[1]+1] == -1:
                break
            elif [pos[0], pos[1]+1] == start:
                break
            else:
                pos = [pos[0], pos[1]+1]
    return score

for t in range(int(input())):
    n = int(input())
    li = [list(map(int, input().split())) for _ in range(n)]
    di = {6:[], 7:[], 8:[], 9:[], 10:[]}
    answer = 0
    for i in range(n):
        for j in range(n):
            if li[i][j] == 6 or li[i][j] == 7 or li[i][j] == 8 or li[i][j] == 9 or li[i][j] == 10:
                di[li[i][j]].append([i, j])
    for i in range(n):
        for j in range(n):
            if li[i][j] == 0:
                answer = max(answer, solve([i, j], 'u'))
                answer = max(answer, solve([i, j], 'd'))
                answer = max(answer, solve([i, j], 'l'))
                answer = max(answer, solve([i, j], 'r'))
    print('#' + str(t+1), str(answer))