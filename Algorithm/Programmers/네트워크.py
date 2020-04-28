def solution(n, computers):
    answer = 0
    save = list()
    for k in range(n):
        if computers[k][k] == 1:
            answer += 1
            save.append(k)
            while len(save) != 0:
                for i in range(n):
                    if computers[save[0]][i] == 1:
                        computers[save[0]][i], computers[i][save[0]] = 0, 0
                        if i not in save:
                            save.append(i)
                if len(save) != 0:
                    del save[0]
    return answer