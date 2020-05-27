# 이분 매칭
def dfs(nNode, n, shark, nMatch, mMatch, visit):
    if visit[nNode]:
        return False
    visit[nNode] = True
    for mNode in range(nNode+1, n):
        if shark[nNode][0] >= shark[mNode][0] and shark[nNode][1] >= shark[mNode][1] and shark[nNode][2] >= shark[mNode][2]:
            if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, shark, nMatch, mMatch, visit):
                nMatch[nNode], mMatch[mNode] = mNode, nNode
                return True
    return False

def bipartiteMatch(n, shark):
    answer = n
    nMatch, mMatch = [-1]*n, [-1]*n
    for nNode in range(n):
        for _ in range(2):
            visit = [False]*n
            if dfs(nNode, n, shark, nMatch, mMatch, visit):
                answer -= 1
    return answer

n = int(input())
shark = []
for _ in range(n):
    shark.append(list(map(int, input().split())))
shark.sort(reverse=True)
print(bipartiteMatch(n, shark))

'''
# 네트워크 플로우(에드몬드 카프)
def solution(start, end):
    global v, capacity, flow, adj
    answer = 0
    while True:
        queue = [start] # 다음에 방문할 정점들
        path = [-1]*v # 방문 경로
        while queue:
            present = queue[0] # 현재 정점
            del queue[0]
            if present not in path:
                for _next in adj[present]:
                    # 흐를 수 있고, 다음 정점이 방문하지 않은 정점일 경우
                    if capacity[present][_next] - flow[present][_next] > 0 and path[_next] == -1:
                        queue.append(_next)
                        path[_next] = present
                        if _next == end: # 다음 방문할 정점이 도착지일 경우
                            break
        if path[end] == -1: # 가능한 모든 경로를 찾았을 경우
            break
        # 역방향
        flowRate = 9876543210 # 현재 경로에서의 최소 유량
        present = end
        while present != start:
            previous = path[present]
            flowRate = min(flowRate, capacity[previous][present] - flow[previous][present])
            present = path[present]
        present = end
        while present != start:
            previous = path[present]
            flow[previous][present] += flowRate
            flow[present][previous] -= flowRate # 음의 유량
            present = path[present]
        answer += flowRate
    return answer

n = int(input()) # 상어 수
v = n*2 + 2 # 정점 수
capacity = [[0]*v for _ in range(v)] # 용량
flow = [[0]*v for _ in range(v)] # 유량
adj = [[] for _ in range(v)] # 연결된 정점(source + 잡아먹는 상어 + 잡아먹히는 상어 + sink)
shark = [] # 상어 스펙
for _ in range(n):
    shark.append(list(map(int, input().split())))
shark.sort(reverse=True)
for _n in range(1, n+1): # source와 잡아먹는 상어 매칭
    adj[0].append(_n)
    adj[_n].append(0)
    capacity[0][_n] = 2 # 한 상어가 최대 두 개의 상어를 먹을 수 있으므로 용량을 2로 설정
for _m in range(n+1, v-1): # 잡아먹히는 상어와 sink 매칭
    adj[_m].append(v-1)
    adj[v-1].append(_m)
    capacity[_m][v-1] = 1
for _n in range(1, n+1): # 잡아먹는 상어와 잡아먹히는 상어 매칭
    for _m in range(_n+1, n+1):
        # 잡아먹는 대상이 자기자신이 아니고, 잡아먹는 상어의 스펙이 잡아먹히는 상어의 스펙보다 크거나 같을 경우
        if _n != _m and shark[_n-1][0] >= shark[_m-1][0] and shark[_n-1][1] >= shark[_m-1][1] and shark[_n-1][2] >= shark[_m-1][2]:
            adj[_n].append(_m+n)
            adj[_m+n].append(_n)
            capacity[_n][_m+n] = 1
print(n - solution(0, v-1))
'''