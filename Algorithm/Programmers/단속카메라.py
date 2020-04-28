def solution(routes):
    answer = 0
    while len(routes):
        remove = list()
        routes.sort(key=lambda x: x[1])
        standard = routes[0][1]
        for i in range(len(routes)):
            if standard >= routes[i][0]:
                remove.append(i)
        remove.sort(reverse=True)
        for i in range(len(remove)):
            del routes[remove[i]]
        answer += 1
    return answer