from itertools import combinations

def solution(relation):
    answer = 0
    save = list()
    combine = list()
    for i in range(len(relation[0])):
        combine += list(combinations([str(j) for j in range(len(relation[0]))], i+1))
    for i in range(len(combine)):
        data = set()
        for row in range(len(relation)):
            tmp = ''
            for col in range(len(combine[i])):
                tmp += relation[row][int(combine[i][col])] + ' '
            data.add(tmp)
        if len(list(data)) == len(relation):
            if len(save) == 0:
                save.append(combine[i])
            else:
                confirm = True
                for a in range(len(save)):
                    count = 0
                    for b in range(len(save[a])):
                        for c in range(len(combine[i])):
                            if combine[i][c] == save[a][b]:
                                count += 1
                    if count == len(save[a]):
                        confirm = False
                        break
                if confirm:
                    save.append(combine[i])
    answer = len(save)
    return answer