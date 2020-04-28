import heapq

def solution(operations):
    answer = 0
    idx = 0
    save = list()
    while idx != len(operations):
        try:
            if operations[idx].split(' ')[0] == 'I':
                heapq.heappush(save, int(operations[idx].split(' ')[1]))
            else:
                if operations[idx].split(' ')[1] == '-1':
                    heapq.heappop(save)
                else:
                    remove = max(save)
                    del save[save.index(remove)]
        except:
            pass
        idx += 1
    if len(save) == 0:
        answer = [0, 0]
    else:
        answer = [max(save), min(save)]
    return answer