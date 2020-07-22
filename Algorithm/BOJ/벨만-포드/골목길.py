import sys
input = sys.stdin.readline

n, m = map(int, input().split())
adj, MIN = [{} for _ in range(n)], -100001
dist, path = [MIN]*n, [-1]*n
plusCycle, visit = [], [0]*n
for _ in range(m):
    a, b, c = map(int, input().split())
    if b-1 in adj[a-1]:
        adj[a-1][b-1] = max(adj[a-1][b-1], c)
    else:
        adj[a-1][b-1] = c
dist[0] = 0
for i in range(n):
    for j in range(n):
        for _next, cost in adj[j].items():
            if dist[j] != MIN and dist[_next] < dist[j]+cost:
                dist[_next], path[_next] = dist[j]+cost, j
                if i == n-1:
                    visit[j] = 1
                    plusCycle.append(j) # 양의 사이클이 발생한 노드 저장
while plusCycle:
    node = plusCycle[0]
    del plusCycle[0]
    for _next, cost in adj[node].items():
        if not visit[_next]:
            visit[_next] = 1
            plusCycle.append(_next)
if path[n-1] == -1 or visit[n-1] == 1: # 출발지에서 목적지까지의 경로가 없거나 양의 사이클에서 독착지까지 도달 가능한 경우
    print(-1)
else:
    idx, answer = n-1, [n]
    while idx != 0:
        answer.append(path[idx]+1)
        idx = path[idx]
    print(' '.join(map(str, answer[::-1])))