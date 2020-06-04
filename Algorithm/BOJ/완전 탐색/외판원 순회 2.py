def TSP(node, visited, cost):
    global n, INF, dist, answer
    if visited == (1<<n) - 1: # 모든 도시를 방문했을 경우
        if dist[node][0] != 0: # 출발지 도시로 돌아갈 수 있는 경우
            answer = min(answer, cost+dist[node][0])
        return
    if cost >= answer: # 현재까지의 이동 비용이 최소 비용보다 크거나 같을 경우
        return
    for next_node in range(n):
        # 이미 방문한 도시이거나 경로가 없는 경우
        if visited & (1<<next_node) or dist[node][next_node] == 0:
            continue
        # 다음 방문 도시를 출발지로 설정하고, 비트 OR 연산을 통해 다음 방문 도시는 방문했다고 설정
        TSP(next_node, visited | (1<<next_node), cost+dist[node][next_node])

n, INF = int(input()), 9876543210 # 도시 개수
dist = [list(map(int, input().split())) for _ in range(n)] # 도시간 이동 비용
answer = INF
TSP(0, 1, 0) # 출발지 도시(0), 출발지 도시는 방문 했다고 설정(1 == 1<<0(출발지 도시))
print(answer)