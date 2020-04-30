def solve(pos, memory, direction):
    global answer
    while not answer:
        if [memory, direction] in visit[pos[1]][pos[0]]:
            break
        else:
            visit[pos[1]][pos[0]].append([memory, direction])
        if li[pos[1]][pos[0]] == '<':
            direction = 'l'
        elif li[pos[1]][pos[0]] == '>':
            direction = 'r'
        elif li[pos[1]][pos[0]] == '^':
            direction = 'u'
        elif li[pos[1]][pos[0]] == 'v':
            direction = 'd'
        elif li[pos[1]][pos[0]] == '_':
            if memory == 0:
                direction = 'r'
            else:
                direction = 'l'
        elif li[pos[1]][pos[0]] == '|':
            if memory == 0:
                direction = 'd'
            else:
                direction = 'u'
        elif li[pos[1]][pos[0]] == '?':
            if direction == 'l':
                solve([pos[0], pos[1]-1 if pos[1]-1 >= 0 else r-1], memory, 'u')
                solve([pos[0], pos[1]+1 if pos[1]+1 < r else 0], memory, 'd')
                solve([pos[0]+1 if pos[0]+1 < c else 0, pos[1]], memory, 'r')
            elif direction == 'r':
                solve([pos[0], pos[1]-1 if pos[1]-1 >= 0 else r-1], memory, 'u')
                solve([pos[0], pos[1]+1 if pos[1]+1 < r else 0], memory, 'd')
                solve([pos[0]-1 if pos[0]-1 >= 0 else c-1, pos[1]], memory, 'l')
            elif direction == 'u':
                solve([pos[0], pos[1]+1 if pos[1]+1 < r else 0], memory, 'd')
                solve([pos[0]-1 if pos[0]-1 >= 0 else c-1, pos[1]], memory, 'l')
                solve([pos[0]+1 if pos[0]+1 < c else 0, pos[1]], memory, 'r')
            else:
                solve([pos[0], pos[1]-1 if pos[1]-1 >= 0 else r-1], memory, 'u')
                solve([pos[0]-1 if pos[0]-1 >= 0 else c-1, pos[1]], memory, 'l')
                solve([pos[0]+1 if pos[0]+1 < c else 0, pos[1]], memory, 'r')
        elif li[pos[1]][pos[0]] == '@':
            answer = True
            break
        elif li[pos[1]][pos[0]] == '+':
            memory = 0 if memory == 15 else memory+1
        elif li[pos[1]][pos[0]] == '-':
            memory = 15 if memory == 0 else memory-1
        else:
            if li[pos[1]][pos[0]] != '.':
                memory = int(li[pos[1]][pos[0]])
        if direction == 'l':
            pos[0] = pos[0]-1 if pos[0]-1 >= 0 else c-1
        elif direction == 'r':
            pos[0] = pos[0]+1 if pos[0]+1 < c else 0
        elif direction == 'u':
            pos[1] = pos[1]-1 if pos[1]-1 >= 0 else r-1
        else:
            pos[1] = pos[1]+1 if pos[1]+1 < r else 0

for t in range(int(input())):
    r, c = map(int, input().split())
    answer = False
    visit = [[[] for j in range(c)] for i in range(r)]
    li = []
    for _ in range(r):
        li.append(list(map(str, input())))
    confirm = []
    for i in range(r):
        for j in range(c):
            if li[i][j] == '@':
                confirm.append([j, i])
    if len(confirm):
        confirm2 = [True]*len(confirm)
        for i in range(len(confirm)):
            x, y = confirm[i][0], confirm[i][1]
            if li[y-1 if y-1 >= 0 else r-1][x] == '^' and li[y+1 if y+1 < r else 0][x] == 'v' and li[y][x-1 if x-1 >= 0 else c-1] == '<' and li[y][x+1 if x+1 < c else 0] == '>':
                confirm2[i] = False
            if li[y-1 if y-1 >= 0 else r-1][x] in '<>' and li[y+1 if y+1 < r else 0][x] in '<>' and li[y][x-1 if x-1 >= 0 else c-1] in '^v' and li[y][x+1 if x+1 < c else 0] in '^v':
                confirm2[i] = False
        if len(set(confirm2)) == 2 or (len(set(confirm2)) == 1 and list(set(confirm2))[0]):
            solve([0, 0], 0, 'r')
    if answer:
        print('#' + str(t+1) + ' YES')
    else:
        print('#' + str(t+1) + ' NO')