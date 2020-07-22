n, m = map(int, input().split())
adj, MAX = [{} for _ in range(n)], 5000001
dist = [MAX]*n
for _ in range(m):
    a, b, c = map(int, input().split())
    if b-1 in adj[a-1]:
        adj[a-1][b-1] = min(adj[a-1][b-1], c)
    else:
        adj[a-1][b-1] = c
dist[0], minusCycle = 0, False
for i in range(n):
    for j in range(n):
        for _next, cost in adj[j].items():
            if dist[j] != MAX and dist[_next] > dist[j]+cost:
                dist[_next] = dist[j]+cost
                if i == n-1:
                    minusCycle = True
if minusCycle:
    print(-1)
else:
    for i in range(1, n):
        if dist[i] == MAX:
            dist[i] = -1
        print(dist[i])