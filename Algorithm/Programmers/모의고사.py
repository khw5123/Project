def solution(answers):
    answer = []
    save = {'1': 0, '2': 0, '3': 0}
    a = [1,2,3,4,5] * 2000
    b = [2,1,2,3,2,4,2,5] * 1250
    c = [3,3,1,1,2,2,4,4,5,5] * 1000
    for i in range(len(answers)):
        if answers[i] == a[i]:
            save['1'] += 1
        if answers[i] == b[i]:
            save['2'] += 1
        if answers[i] == c[i]:
            save['3'] += 1
    tmp = sorted(save.items(), key=lambda x: x[1], reverse=True)
    for el in tmp:
        if el[1] == tmp[0][1]:
            answer.append(int(el[0]))
    return answer