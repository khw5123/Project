def dfs(n, m, s, arr):
    stack = [s]
    dfs = []
    while stack:
        # print(stack)
        visit = stack.pop()
        # print(visit)
        if visit not in dfs:
            dfs.append(visit)
            tmp = []
            for i in range(len(arr)):
                if arr[i][0] == visit:
                    tmp.append(arr[i][1])
                if arr[i][1] == visit:
                    tmp.append(arr[i][0])
            tmp.sort(reverse=True)
            for i in tmp:
                stack.append(i)
    return dfs

def bfs(n, m, s, arr):
    queue = [s]
    bfs = []
    while queue:
        # print(queue)
        visit = queue[0]
        del queue[0]
        # print(visit)
        if visit not in bfs:
            bfs.append(visit)
            tmp = []
            for i in range(len(arr)):
                if arr[i][0] == visit:
                    tmp.append(arr[i][1])
                if arr[i][1] == visit:
                    tmp.append(arr[i][0])
            tmp.sort()
            for i in tmp:
                queue.append(i)
    return bfs

n, m, s = map(int, input().split())
arr = []
for i in range(m):
    num = input()
    arr.append([int(num.split(' ')[0]), int(num.split(' ')[1])])
dfs = dfs(n, m, s, arr)
bfs = bfs(n, m, s, arr)
for num in dfs:
    print(num, end=' ')
print()
for num in bfs:
    print(num, end=' ')