import sys
input = sys.stdin.readline

def getDistance(start):
    ret = 0
    queue = [[start, 0]]
    visit = []
    while queue:
        node, length = queue[0][0], queue[0][1]
        del queue[0]
        ret = max(ret, length)
        if node not in visit:
            visit.append(node)
            for _next in adj[node]:
                queue.append([_next, length+distance[node][_next]])
    return ret

n = int(input())
adj = [[] for _ in range(n+1)]
distance = [{} for _ in range(n+1)]
dp = [-1]*(n+1)
answer = 0
for _ in range(n-1):
    a, b, d = map(int, input().split())
    adj[a].append(b)
    distance[a][b] = d
for node in range(n, 0, -1):
    if adj[node]:
        dist = []
        for _next in adj[node]:
            ret = distance[node][_next]
            if dp[_next] != -1:
                ret += dp[_next]
            else:
                ret += getDistance(_next)
            dist.append(ret)
        dist.sort(reverse=True)
        dp[node] = dist[0]
        answer = max(answer, sum(dist[:2]))
print(answer)