import sys
input = sys.stdin.readline

def topologicalSort():
    global v
    answer, result, queue = '', [], []
    for i in range(1, v+1):
        if indegree[i] == 0: # 들어오는 간선이 없는 정점 큐에 저장
            queue.append(i)
    for i in range(1, v+1):
        if not queue: # 도중에 큐가 비면 위상 정렬 불가능(사이클 존재)
            return 'IMPOSSIBLE'
        if len(queue) > 1: # 위상 정렬의 결과가 2개 이상일 경우
            answer = '?'
        node = queue[0] # 현재 정점
        del queue[0]
        result.append(node)
        for _next in adj[node]: # 현재 정점과 인접한 정점들
            indegree[_next] -= 1 # 인접한 정점의 indegree 감소
            if indegree[_next] == 0: # 인접한 정점으로 들어오는 간선이 없으면 인접한 정점 큐에 저장
                queue.append(_next)
    if answer == '':
        for v in result:
            answer += (str(v) + ' ')
    return answer

for _ in range(int(input())):
    v = int(input())
    indegree = [0]*(v+1) # 정점별 들어오는 간선의 수
    adj = [[] for _ in range(v+1)]
    lastScore = list(map(int, input().split())) # 작년 등수
    for i in range(v-1):
        for j in range(i+1, v):
            # 작년 등수를 기반으로 순위 구성
            indegree[lastScore[j]] += 1
            adj[lastScore[i]].append(lastScore[j])
    for _ in range(int(input())):
        a, b = map(int, input().split())
        if b in adj[a]: # a가 b보다 등수가 높았던 경우
            # a가 b 보다 높았던 기록 삭제
            indegree[b] -= 1
            adj[a].remove(b)
            # 등수 교체
            indegree[a] += 1
            adj[b].append(a)
        else: # b가 a보다 등수가 높았던 경우
            # b가 a보다 높았던 기록 삭제
            indegree[a] -= 1
            adj[b].remove(a)
            # 등수 교체
            indegree[b] += 1
            adj[a].append(b)
    answer = topologicalSort()
    print(answer)