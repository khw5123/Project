def solution(s):
    answer = []
    save = []
    num = ''
    for i in range(len(s)):
        if i == 0 or i == len(s)-1:
            continue
        if s[i] == '{':
            save.append([])
        elif s[i] == '}' or s[i] == ',':
            if num != '':
                save[-1].append(int(num))
                num = ''
        else:
            num += s[i]
    save.sort(key=len)
    if len(save) == 1:
        answer.append(save[0][0])
    else:
        answer.append(save[0][0])
        for i in range(1, len(save)):
            for j in range(len(save[i])):
                if save[i][j] not in answer:
                    answer.append(save[i][j])
                    break
    return answer