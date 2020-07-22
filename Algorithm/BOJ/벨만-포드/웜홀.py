import sys
input = sys.stdin.readline

for _ in range(int(input())):
    n, m, w = map(int, input().split())
    adj, MAX = [[] for _ in range(n)], 5000001
    dist = [MAX]*n
    for _ in range(m):
        s, e, t = map(int, input().split())
        adj[s-1].append((e-1, t))
        adj[e-1].append((s-1, t))
    for _ in range(w):
        s, e, t = map(int, input().split())
        adj[s-1].append((e-1, -t))
    dist[0], minusCycle = 0, 'NO'
    for i in range(n):
        for j in range(n):
            for _next, cost in adj[j]:
                # 최단 거리를 구하는 것이 아니라 음의 사이클 유무만 파악하는 것이므로 두 노드가 단절되어 있는지(dist[j] != MAX) 확인할 필요 없음
                if dist[_next] > dist[j]+cost:
                    dist[_next] = dist[j]+cost
                    if i == n-1:
                        minusCycle = 'YES'
    print(minusCycle)