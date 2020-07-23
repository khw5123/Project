n, s, e, m = map(int, input().split())
adj, MIN = [[] for _ in range(n)], -100000001
dist, path = [MIN]*n, [-1]*n
plusCycle, visit = [], [0]*n
for _ in range(m):
    a, b, c = map(int, input().split())
    adj[a].append((b, -c))
revenue = list(map(int, input().split()))
dist[s], path[s] = revenue[s], -2
for i in range(n):
    for j in range(n):
        for _next, cost in adj[j]:
            if dist[j] != MIN and dist[_next] < dist[j] + cost + revenue[_next]:
                dist[_next], path[_next] = dist[j] + cost + revenue[_next], j
                if i == n-1:
                    visit[j] = 1
                    plusCycle.append(j) # 양의 사이클이 발생한 노드 저장
while plusCycle:
    node = plusCycle[0]
    del plusCycle[0]
    for _next, cost in adj[node]:
        if not visit[_next]:
            visit[_next] = 1
            plusCycle.append(_next)
if path[e] == -1: # 도착 도시에 도착하는 것이 불가능한 경우(출발지에서 목적지까지의 경로가 없는 경우)
    print('gg')
elif visit[e] == 1: # 돈을 무한히 많이 가지고 있을 수 있는 경우(양의 사이클에서 독착지까지 도달 가능한 경우)
    print('Gee')
else:
    print(dist[e])