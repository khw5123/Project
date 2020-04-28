def solution(participant, completion):
    answer = ''
    p, c = set(participant), set(completion)
    if len(p - c) == 0:
        di = dict()
        for i in range(len(participant)):
            if participant[i] in di:
                di[participant[i]] += 1
            else:
                di[participant[i]] = 1
        for k, v in di.items():
            if v > 1:
                if participant.count(k) - completion.count(k) == 1:
                    answer = k
                    break
    else:
        answer = list(p - c)[0]
    return answer