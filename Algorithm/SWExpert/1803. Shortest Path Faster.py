import heapq

def solve(start_node):
    dist = [pow(10, 15)]*(n+1)
    dist[start_node] = 0
    pq = []
    heapq.heappush(pq, [0, start_node])
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        for next_node, weight in li[current_node].items():
            next_dist = dist[current_node] + weight
            if next_dist < dist[next_node]:
                dist[next_node] = next_dist
                heapq.heappush(pq, [next_dist, next_node])
    return dist

for t in range(int(input())):
    n, m, s, e = map(int, input().split())
    li = [dict() for _ in range(n+1)]
    for _ in range(m):
        a, b, w = map(int, input().split())
        li[a][b], li[b][a] = w, w
    answer = solve(s)
    print('#' + str(t+1), str(answer[e]))