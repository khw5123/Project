def solution(n, lost, reserve):
    answer = 0
    lost.sort()
    reserve.sort()
    remove = list()
    impossible = list()
    remain = list()
    for r in reserve:
        if r in lost:
            remove.append(r)
    for r in remove:
        if r in lost:
            lost.remove(r)
            reserve.remove(r)
    for i in range(len(lost)):
        confirm = False
        for r in reserve:
            if lost[i]-1 == r or lost[i]+1 == r:
                if r not in remain:
                    remain.append(r)
                confirm = True
        if confirm == False:
            impossible.append(lost[i])
    for i in impossible:
        lost.remove(i)
    reserve = list(set(reserve) & set(remain))
    reserve.sort()
    while len(reserve) != 0:
        remove = list()
        for i in range(len(reserve)):
            if reserve[i]-1 in lost and reserve[i]+1 in lost:
                if reserve[i]-2 in reserve and reserve[i]+2 not in reserve:
                    remove.append([reserve[i]+1, reserve[i]])
                elif reserve[i]-2 not in reserve and reserve[i]+2 in reserve:
                    remove.append([reserve[i]-1, reserve[i]])
                elif (reserve[i]-2 in reserve and reserve[i]+2 in reserve) \
                    or (reserve[i]-2 not in reserve and reserve[i]+2 not in reserve):
                        remove.append([reserve[i]-1, reserve[i]])
            elif reserve[i]-1 in lost and reserve[i]+1 not in lost:
                remove.append([reserve[i]-1, reserve[i]])
            elif reserve[i]-1 not in lost and reserve[i]+1 in lost:
                remove.append([reserve[i]+1, reserve[i]])
        for r in remove:
            try:
                reserve.remove(r[1])
                lost.remove(r[0])
            except:
                pass
    answer = n - (len(impossible) + len(lost))
    return answer