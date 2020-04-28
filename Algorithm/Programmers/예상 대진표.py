import copy

def solution(n,a,b):
    answer = 0
    save, tmp = list(), list()
    for i in range(1, n+1):
        if i == a or i == b:
            save.append([i, 1])
        else:
            save.append([i, 0])
    end = True
    while end:
        answer += 1
        for i in range(0, len(save), 2):
            if save[i][1] == 0 and save[i+1][1] == 0:
                tmp.append([save[i][0], 0])
            else:
                if save[i][1] == 1 and save[i+1][1] == 1:
                    end = False
                    break
                else:
                    if save[i][1] == 1:
                        tmp.append([save[i][0], 1])
                    elif save[i+1][1] == 1:
                        tmp.append([save[i+1][0], 1])
        save = copy.deepcopy(tmp)
        tmp = copy.deepcopy([])
    return answer