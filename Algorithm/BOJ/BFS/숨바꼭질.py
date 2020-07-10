MAX = 100000
n, k = map(int, input().split())
queue, dp = [n], [0]*(MAX+1)
while queue:
    x = queue[0]
    del queue[0]
    if x == k:
        print(dp[x])
        break
    for nx in [x-1, x+1, x*2]:
        if 0 <= nx <= MAX and not dp[nx]:
            dp[nx] = dp[x]+1
            queue.append(nx)
'''
MAX = 100000
n, k = map(int, input().split())
queue, visit = [[n, 0]], [0]*(MAX+1)
while queue:
    x, time = queue[0][0], queue[0][1]
    del queue[0]
    if x == k:
        print(time)
        break
    if visit[x] == 0 or visit[x] > time:
        visit[x] = time
        if x-1 >= 0:
            queue.append([x-1, time+1])
        if x+1 < len(visit):
            queue.append([x+1, time+1])
        if x*2 < len(visit):
            queue.append([x*2, time+1])
'''