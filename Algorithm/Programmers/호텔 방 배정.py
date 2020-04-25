def solution(k, room_number):
    answer = []
    occupy = dict()
    for n in room_number:
        if n not in occupy:
            answer.append(n)
            occupy[n] = n+1
        else:
            p = n
            visit = []
            while True:
                if p in occupy:
                    visit.append(p)
                    p = occupy[p]
                else:
                    answer.append(p)
                    occupy[p] = p+1
                    for v in visit:
                        occupy[v] = p+1
                    break
    return answer