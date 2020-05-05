import operator
import heapq

def solve(start_node):
    dist = [1000]*n
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
    tmp = list(map(int, input().split()))
    n = tmp[0]
    save = [[0]*n for _ in range(n)]
    li = [dict() for _ in range(n)]
    answer = [0]*n
    row = 0
    for i in range(1, len(tmp)):
        save[row//n][i-row-1] = tmp[i]
        if i % n == 0:
            row += n
    for i in range(n):
        for j in range(n):
            if save[i][j] != 0:
                li[i][j] = save[i][j]
    for start in range(n):
        answer = list(map(operator.add, answer, solve(start)))
    print('#' + str(t+1), min(answer))