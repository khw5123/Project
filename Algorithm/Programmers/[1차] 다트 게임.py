def solution(dartResult):
    answer = 0
    ranges = {'S':1, 'D':2, 'T':3}
    save = list()
    result = list()
    line = 0
    for i in range(len(dartResult)):
        if dartResult[i] in ranges:
            if i+1 < len(dartResult) and dartResult[i+1] in '*#':
                save.append(dartResult[line:i+2])
                line = i+2
            else:
                save.append(dartResult[line:i+1])
                line = i+1
    for i in range(len(save)):
        if '*' in save[i]:
            if i == 0:
                result.append(pow(int(save[i].split(save[i][-2])[0]), ranges[save[i][-2]]) * 2)
            else:
               result[-1] *= 2
               result.append(pow(int(save[i].split(save[i][-2])[0]), ranges[save[i][-2]]) * 2)
        elif '#' in save[i]:
            result.append(pow(int(save[i].split(save[i][-2])[0]), ranges[save[i][-2]]) * -1)
        else:
            result.append(pow(int(save[i].split(save[i][-1])[0]), ranges[save[i][-1]]))
    answer = sum(result)
    return answer