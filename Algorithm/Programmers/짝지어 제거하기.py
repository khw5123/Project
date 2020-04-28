def solution(string):
    answer = 0
    save = list()
    for c in string:
        if len(save) == 0:
            save.append(c)
        else:
            if save[-1] == c:
                save.pop()
            else:
                save.append(c)
    if len(save) == 0:
        answer = 1
    else:
        answer = 0
    return answer