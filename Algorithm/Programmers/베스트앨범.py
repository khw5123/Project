def solution(genres, plays):
    answer = []
    di = dict()
    for i in range(len(plays)):
        if genres[i] not in di:
            di[genres[i]] = plays[i]
        else:
            di[genres[i]] += plays[i]
    save = list()
    for k, v in di.items():
        save.append([v, k])
    save.sort(reverse=True)
    for i in range(len(save)):
        genre = save[i][1]
        tmp = list()
        for j in range(len(genres)):
            if genres[j] == genre:
                tmp.append([plays[j], j])
        tmp.sort(key=lambda x:(-x[0],x[1]))
        if len(tmp) == 1:
            answer.append(tmp[0][1])
        else:
            answer.append(tmp[0][1])
            answer.append(tmp[1][1])
    return answer