def find(a, li):
    if a == li[a]:
        return a
    else:
        li[a] = find(li[a], li)
        return li[a]

def union(a, b, li):
    a, b = find(a, li), find(b, li)
    if a == b:
        return False
    else:
        li[a] = b
        return True

def solution(land, height):
    answer = 0
    li = [i for i in range(len(land)*len(land[0])+1)]
    edge = []
    count = 1
    for i in range(len(land)):
        for j in range(len(land[0])):
            if i == len(land)-1 and j == len(land[0])-1:
                continue
            else:
                if i == len(land)-1:
                    edge.append([count, count+1, abs(land[i][j] - land[i][j+1])])
                elif j == len(land[0])-1:
                    edge.append([count, count+len(land[0]), abs(land[i][j] - land[i+1][j])])
                else:
                    edge.append([count, count+1, abs(land[i][j] - land[i][j+1])])
                    edge.append([count, count+len(land[0]), abs(land[i][j] - land[i+1][j])])
            count += 1
    edge.sort(key=lambda x:x[2])
    for i in range(len(edge)):
        if union(edge[i][0], edge[i][1], li):
            if edge[i][2] > height:
                answer += edge[i][2]
    return answer

'''
def solution(land, height):
    answer = 0
    queue, visit, next_ = [[0, 0]], [], []
    dp = [[[-1, -1, -1, -1, 0] for _ in range(len(land[0]))] for _ in range(len(land))]
    while len(visit) != len(land)*len(land[0]):
        if len(queue) == 0:
            if next_[-1][2] == 0:
                queue = [[next_[-1][0]-1, next_[-1][1]]]
            elif next_[-1][2] == 1:
                queue = [[next_[-1][0]+1, next_[-1][1]]]
            elif next_[-1][2] == 2:
                queue = [[next_[-1][0], next_[-1][1]-1]]
            else:
                queue = [[next_[-1][0], next_[-1][1]+1]]
            answer += next_[-1][3]
            dp[next_[-1][1]][next_[-1][0]][next_[-1][2]] = -1
            next_.pop()
        while queue:
            x, y = queue[0][0], queue[0][1]
            del queue[0]
            if dp[y][x][4] == 0:
                dp[y][x][4] = 1
                visit.append((x, y))
                if x-1 >= 0:
                    if dp[y][x-1][4] == 0:
                        if height < abs(land[y][x] - land[y][x-1]):
                            dp[y][x][0] = abs(land[y][x] - land[y][x-1])
                            next_.append([x, y, 0, dp[y][x][0]])
                        if height >= abs(land[y][x] - land[y][x-1]):
                            queue.append([x-1, y])
                if x+1 < len(land[0]):
                    if dp[y][x+1][4] == 0:
                        if height < abs(land[y][x] - land[y][x+1]):
                            dp[y][x][1] = abs(land[y][x] - land[y][x+1])
                            next_.append([x, y, 1, dp[y][x][1]])
                        if height >= abs(land[y][x] - land[y][x+1]):
                            queue.append([x+1, y])
                if y-1 >= 0:
                    if dp[y-1][x][4] == 0:
                        if height < abs(land[y][x] - land[y-1][x]):
                            dp[y][x][2] = abs(land[y][x] - land[y-1][x])
                            next_.append([x, y, 2, dp[y][x][2]])
                        if height >= abs(land[y][x] - land[y-1][x]):
                            queue.append([x, y-1])
                if y+1 < len(land):
                    if dp[y+1][x][4] == 0:
                        if height < abs(land[y][x] - land[y+1][x]):
                            dp[y][x][3] = abs(land[y][x] - land[y+1][x])
                            next_.append([x, y, 3, dp[y][x][3]])
                        if height >= abs(land[y][x] - land[y+1][x]):
                            queue.append([x, y+1])
        remove = []
        for i in range(len(next_)):
            if next_[i][2] == 0:
                if dp[next_[i][1]][next_[i][0]-1][4] == 1:
                    remove.append(i)
            elif next_[i][2] == 1:
                if dp[next_[i][1]][next_[i][0]+1][4] == 1:
                    remove.append(i)
            elif next_[i][2] == 2:
                if dp[next_[i][1]-1][next_[i][0]][4] == 1:
                    remove.append(i)
            else:
                if dp[next_[i][1]+1][next_[i][0]][4] == 1:
                    remove.append(i)
        remove.reverse()
        for idx in remove:
            del next_[idx]
        next_.sort(key=lambda x:-x[3])
    return answer
'''