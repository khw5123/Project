def topologicalSort():
    result, queue = [0]*(v+1), []
    for i in range(1, v+1):
        if indegree[i] == 0: # 들어오는 간선이 없는 정점 큐에 저장
            queue.append(i)
            result[i] = cost[i] # 건물을 짓는데 걸리는 시간 추가
    for i in range(1, v+1):
        if not queue: # 도중에 큐가 비면 위상 정렬 불가능(사이클 존재)
            return []
        node = queue[0] # 현재 정점
        del queue[0]
        for _next in adj[node]: # 현재 정점과 인접한 정점들
            indegree[_next] -= 1 # 인접한 정점의 indegree 감소
            result[_next] = max(result[_next], result[node]+cost[_next]) # 정점별 건물을 짓는데 걸리는 최소 시간
            if indegree[_next] == 0: # 인접한 정점으로 들어오는 간선이 없으면 인접한 정점 큐에 저장
                queue.append(_next)
    return result

v = int(input())
indegree = [0]*(v+1) # 정점별 들어오는 간선의 수
adj = [[] for _ in range(v+1)]
cost = [0]*(v+1) # 정점별 건물을 짓는데 걸리는 시간
for node in range(1, v+1):
    info = list(map(int, input().split()))
    cost[node] = info[0]
    for i in range(1, len(info)-1):
        indegree[node] += 1
        adj[info[i]].append(node)
answer = topologicalSort()
for i in range(1, len(answer)):
    print(answer[i])