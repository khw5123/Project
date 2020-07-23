import sys
import heapq
input = sys.stdin.readline
INF = 9876543210

def dijkstra(start_node):
    dist, pq = [INF]*(v+1), []
    dist[start_node] = 0
    heapq.heappush(pq, [0, start_node])
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        for next_node, weight in adj[current_node].items():
            next_dist = dist[current_node] + weight
            if dist[next_node] > next_dist:
                dist[next_node] = next_dist
                heapq.heappush(pq, [next_dist, next_node])
    return dist

for _ in range(int(input())):
    v, e, t = map(int, input().split())
    s, g, h = map(int, input().split())
    adj, dst = [{} for _ in range(v+1)], []
    answer = []
    for _ in range(e):
        a, b, d = map(int, input().split())
        if (a == g and b == h) or (a == h and b == g):
            adj[a][b], adj[b][a] = d*2 - 1, d*2 - 1
        else:
            adj[a][b], adj[b][a] = d*2, d*2
    for _ in range(t):
        dst.append(int(input()))
    dist = dijkstra(s)
    for end_node in dst:
        if dist[end_node] != INF and dist[end_node] % 2:
            answer.append(end_node)
    print(' '.join(map(str, sorted(answer))))