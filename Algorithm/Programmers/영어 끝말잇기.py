import math

def solution(n, words):
    answer = []
    save = list()
    for i in range(len(words)):
        if len(save) != 0 and (words[i] in save or save[-1][len(save[-1])-1:] != words[i][0]):
            answer.append((i % n) + 1)
            answer.append(math.ceil((i + 1) / n))
            break
        else:
            save.append(words[i])
    if len(answer) == 0:
        answer.append(0)
        answer.append(0)
    return answer