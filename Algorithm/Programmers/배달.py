import heapq

def solve(start_node, li, N, road):
    dist = [500001]*(N+1)
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

def solution(N, road, K):
    answer = 0
    li = [dict() for _ in range(N+1)]
    for i in range(len(road)):
        if road[i][1] in li[road[i][0]]:
            li[road[i][0]][road[i][1]] = min(li[road[i][0]][road[i][1]], road[i][2])
        else:
            li[road[i][0]][road[i][1]] = road[i][2]
        if road[i][0] in li[road[i][1]]:
            li[road[i][1]][road[i][0]] = min(li[road[i][1]][road[i][0]], road[i][2])
        else:
            li[road[i][1]][road[i][0]] = road[i][2]
    for v in solve(1, li, N, road):
        if v <= K:
            answer += 1
    return answer