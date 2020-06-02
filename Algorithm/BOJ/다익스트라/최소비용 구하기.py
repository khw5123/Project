import sys
import heapq
input = sys.stdin.readline

def solution(start_node):
    dist = [INF]*(v+1)
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

v, INF = int(input()), 9876543210
li = [dict() for _ in range(v+1)]
for _ in range(int(input())):
    a, b, w = map(int, input().split())
    if b in li[a]:
        li[a][b] = min(li[a][b], w)
    else:
        li[a][b] = w
start, end = map(int, input().split())
answer = solution(start)[end]
print(answer)