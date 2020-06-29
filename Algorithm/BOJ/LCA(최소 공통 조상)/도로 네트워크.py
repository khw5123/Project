import sys
import math
input = sys.stdin.readline

def makeTree(start):
    queue, visit = [start], [False]*n
    while queue:
        node = queue[0]
        del queue[0]
        if not visit[node]:
            visit[node] = True
            for _next in adj[node]:
                if depth[_next] == -1:
                    parent[_next][0] = node
                    depth[_next] = depth[node]+1
                    # 현재 노드와 연결된 노드 사이의 거리 저장 
                    _min[_next][0] = distance[node][_next]
                    _max[_next][0] = distance[node][_next]
                    queue.append(_next)

n = int(input())
adj = [[] for _ in range(n)]
parent = [[-1]*round(math.log2(n)) for _ in range(n)]
depth = [0] + [-1]*(n-1)
distance = [dict() for _ in range(n)]
_min = [[math.inf]*round(math.log2(n)) for _ in range(n)]
_max = [[-1]*round(math.log2(n)) for _ in range(n)]
for _ in range(n-1):
    a, b, d = map(int, input().split())
    adj[a-1].append(b-1)
    adj[b-1].append(a-1)
    distance[a-1][b-1], distance[b-1][a-1] = d, d
makeTree(0)
for j in range(1, len(parent[0])):
    for i in range(1, n):
        if parent[i][j-1] != -1:
            parent[i][j] = parent[parent[i][j-1]][j-1]
            # 노드 사이의 최소, 최대 거리도 희소 테이블에 저장
            _min[i][j] = min(_min[i][j-1], _min[parent[i][j-1]][j-1])
            _max[i][j] = max(_max[i][j-1], _max[parent[i][j-1]][j-1])
for _ in range(int(input())):
    answer = [math.inf, 0]
    a, b = map(int, input().split())
    a, b = a-1, b-1
    if depth[a] < depth[b]: # b노드의 깊이가 더 깊을 경우
        a, b = b, a # a노드를 더 깊은 노드로 변경
    diff = depth[a]-depth[b] # 깊이 차이
    for i in range(len(parent[0])):
        if diff | 1<<i == diff: # 두 노드의 깊이 차이가 있을 경우
            # 현재 노드(a)와 부모 노드 사이의 거리 비교
            answer[0] = min(answer[0], _min[a][i])
            answer[1] = max(answer[1], _max[a][i])
            a = parent[a][i] # 깊은 노드(a노드)를 위로 올림
    if a != b: # 두 노드가 같지 않을 경우(같으면 최소 공통 조상임)
        # 두 노드는 같은 깊이를 유지함
        for i in range(len(parent[0])-1, -1, -1): # 큰 값부터 순회하면서 최소 공통 조상 찾음
            if parent[a][i] != -1 and parent[a][i] != parent[b][i]: # 두 노드의 부모가 같지 않을 경우
                # 현재 노드(a, b)와 부모 노드 사이의 거리 비교
                answer[0] = min(answer[0], min(_min[a][i], _min[b][i]))
                answer[1] = max(answer[1], max(_max[a][i], _max[b][i]))
                a, b = parent[a][i], parent[b][i] # 두 노드를 위로 올림
        # 현재 노드(a, b)와 부모 노드(최소 공통 조상 노드) 사이의 거리도 비교해줘야 함
        answer[0] = min(answer[0], min(_min[a][0], _min[b][0]))
        answer[1] = max(answer[1], max(_max[a][0], _max[b][0]))
    print(answer[0], answer[1])