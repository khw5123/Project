def solution(n, costs):
    answer = 0
    costs.sort(key=lambda cost:(cost[2]))
    vertex = [costs[0][0]]
    while len(vertex) != n:
        cost, idx = 987654321, 0
        for i in range(len(costs)):
            if costs[i][0] in vertex or costs[i][1] in vertex:
                if costs[i][0] not in vertex or costs[i][1] not in vertex:
                    if cost > costs[i][2]:
                        cost = costs[i][2]
                        idx = i
        answer += cost
        vertex.append(costs[idx][0])
        vertex.append(costs[idx][1])
        vertex = list(set(vertex))
        costs.pop(idx)
    return answer