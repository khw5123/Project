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

n, m = map(int, input().split())
v, INF = n*m, 9876543210
li = [dict() for _ in range(v+1)]
maze = [list(input()) for _ in range(m)]
node = [[0]*n for _ in range(m)]
num = 1
for i in range(m):
    for j in range(n):
        node[i][j] = num
        num += 1
for i in range(m):
    for j in range(n):
        if i-1 >= 0:
            if maze[i-1][j] == '1':
                li[node[i][j]][node[i-1][j]] = 1
            else:
                li[node[i][j]][node[i-1][j]] = 0
        if i+1 < m:
            if maze[i+1][j] == '1':
                li[node[i][j]][node[i+1][j]] = 1
            else:
                li[node[i][j]][node[i+1][j]] = 0
        if j-1 >= 0:
            if maze[i][j-1] == '1':
                li[node[i][j]][node[i][j-1]] = 1
            else:
                li[node[i][j]][node[i][j-1]] = 0
        if j+1 < n:
            if maze[i][j+1] == '1':
                li[node[i][j]][node[i][j+1]] = 1
            else:
                li[node[i][j]][node[i][j+1]] = 0
start, end = 1, n*m
answer = solution(start)[end]
print(answer)