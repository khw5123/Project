import sys
input = sys.stdin.readline

def topologicalSort():
    result, queue = [], []
    for i in range(1, v+1):
        if indegree[i] == 0: # 들어오는 간선이 없는 정점 큐에 저장
            queue.append(i)
    for i in range(1, v+1):
        if not queue: # 도중에 큐가 비면 위상 정렬 불가능(사이클 존재)
            return []
        node = queue[0] # 현재 정점
        del queue[0]
        result.append(node)
        for _next in adj[node]: # 현재 정점과 인접한 정점들
            indegree[_next] -= 1 # 인접한 정점의 indegree 감소
            if indegree[_next] == 0: # 인접한 정점으로 들어오는 간선이 없으면 인접한 정점 큐에 저장
                queue.append(_next)
    return result

v, m = map(int, input().split())
indegree = [0]*(v+1) # 정점별 들어오는 간선의 수
adj = [[] for _ in range(v+1)]
for _ in range(m):
    a, b = map(int, input().split())
    indegree[b] += 1
    adj[a].append(b)
answer = topologicalSort()
for v in answer:
    print(v, end=' ')
print()