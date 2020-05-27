def solution(start, end):
    global v, capacity, flow, adj
    answer = 0
    while True:
        queue = [start] # 다음에 방문할 정점들
        path = [-1]*v # 방문 경로
        while queue:
            present = queue[0] # 현재 정점
            del queue[0]
            if present not in path:
                for _next in adj[present]:
                    # 흐를 수 있고, 다음 정점이 방문하지 않은 정점일 경우
                    if capacity[present][_next] - flow[present][_next] > 0 and path[_next] == -1:
                        queue.append(_next)
                        path[_next] = present
                        if _next == end: # 다음 방문할 정점이 도착지일 경우
                            break
        if path[end] == -1: # 가능한 모든 경로를 찾았을 경우
            break
        # 역방향
        flowRate = 9876543210 # 현재 경로에서의 최소 유량
        present = end
        while present != start:
            previous = path[present]
            flowRate = min(flowRate, capacity[previous][present] - flow[previous][present])
            present = path[present]
        present = end
        while present != start:
            previous = path[present]
            flow[previous][present] += flowRate
            flow[present][previous] -= flowRate # 음의 유량
            present = path[present]
        answer += flowRate
    return answer

v, e = 52, int(input()) # 정점, 간선 수
capacity = [[0]*v for _ in range(v)] # 용량
flow = [[0]*v for _ in range(v)] # 유량
adj = [[] for _ in range(v)] # 연결된 정점
for _ in range(e):
    _from, to, _capacity = map(str, input().split())
    _from, to, _capacity = (ord(_from)-97+26 if ord(_from) >= 97 else ord(_from)-65), (ord(to)-97+26 if ord(to) >= 97 else ord(to)-65), int(_capacity)
    adj[_from].append(to)
    adj[to].append(_from)
    capacity[_from][to] += _capacity
    capacity[to][_from] += _capacity
print(solution(0, v//2-1))