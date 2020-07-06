def solution(gems):
    answer, name, count, tmp = list(), dict(), set(), 0
    for gem in gems:
        if gem not in name:
            name[gem] = tmp
            tmp += 1
    li, end = [0]*len(name), 0
    for start in range(len(gems)):
        while len(count) != len(name) and end < len(gems):
            li[name[gems[end]]] += 1
            count.add(gems[end])
            end += 1
        if len(count) == len(name):
            if not answer or (answer and end-start < answer[1]-answer[0]+1):
                answer = [start+1, end]
        li[name[gems[start]]] -= 1
        if li[name[gems[start]]] == 0:
            count.remove(gems[start])
    return answer