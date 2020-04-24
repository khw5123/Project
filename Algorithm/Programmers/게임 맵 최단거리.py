def solution(maps):
    answer = -1
    queue, visit = [[0, 0, 1]], dict()
    while queue:
        x, y, count = queue[0][0], queue[0][1], queue[0][2]
        del queue[0]
        if [x, y] == [len(maps[0])-1, len(maps)-1]:
            answer = count
            break
        if (x, y) not in visit:
            visit[(x, y)] = count
            for d in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                dx, dy = x+d[0], y+d[1]
                if 0 <= dx and dx < len(maps[0]) and 0 <= dy and dy < len(maps):
                    if maps[dy][dx] == 1:
                        queue.append([dx, dy, count+1])
    return answer

def solution(maps):
    queue = [[0, 0, 1]]
    while queue:
        x, y, count = queue[0][0], queue[0][1], queue[0][2]
        del queue[0]
        for d in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            dx, dy = x+d[0], y+d[1]
            if 0 <= dx and dx < len(maps[0]) and 0 <= dy and dy < len(maps):
                if [dx, dy] == [len(maps[0])-1, len(maps)-1]:
                    return count+1
                if maps[dy][dx] == 1:
                    maps[dy][dx] = 0
                    queue.append([dx, dy, count+1])
    return -1