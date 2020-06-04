def TSP(node, visited):
    global n, INF, dist, dp
    if visited == (1<<n) - 1: # 모든 도시를 방문했을 경우
        if dist[node][0] != 0: # 출발지 도시로 돌아갈 수 있는 경우
            return dist[node][0]
        else:
            return INF
    if dp[node][visited] != -1: # 이미 방문한 도시인 경우
        return dp[node][visited]
    dp[node][visited] = INF
    for next_node in range(n):
        # 이미 방문한 도시이거나 경로가 없는 경우
        if visited & (1<<next_node) or dist[node][next_node] == 0:
            continue
        # 다음 방문 도시를 출발지로 설정하고, 비트 OR 연산을 통해 다음 방문 도시는 방문했다고 설정
        dp[node][visited] = min(dp[node][visited], TSP(next_node, visited | (1<<next_node)) + dist[node][next_node]) # 최소 비용
    return dp[node][visited]

n, INF = int(input()), 9876543210 # 도시 개수
dist = [list(map(int, input().split())) for _ in range(n)] # 도시간 이동 비용
dp = [[-1]*(1<<n) for _ in range(n)] # 메모이제이션
print(TSP(0, 1)) # 출발지 도시(0), 출발지 도시는 방문 했다고 설정(1 == 1<<0(출발지 도시))