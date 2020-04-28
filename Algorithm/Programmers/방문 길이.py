def solution(dirs):
    answer = 0
    move = list()
    size = 11
    x, y = size // 2, size // 2
    for dir_ in dirs:
        tmp = (x,y)
        if dir_ == 'U':
            if y != 0:
                y -= 1
                if [tmp, (x,y)] not in move:
                    move.append([tmp, (x,y)])
                    move.append([(x,y), tmp])
        elif dir_ == 'D':
            if y != size-1:
                y += 1
                if [tmp, (x,y)] not in move:
                    move.append([tmp, (x,y)])
                    move.append([(x,y), tmp])
        elif dir_ == 'L':
            if x != 0:
                x -= 1
                if [tmp, (x,y)] not in move:
                    move.append([tmp, (x,y)])
                    move.append([(x,y), tmp])
        else:
            if x != size-1:
                x += 1
                if [tmp, (x,y)] not in move:
                    move.append([tmp, (x,y)])
                    move.append([(x,y), tmp])
    answer = len(move) // 2
    return answer