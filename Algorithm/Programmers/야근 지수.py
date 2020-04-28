import heapq

def solution(n, works):
    answer = 0
    count = 0
    save = list()
    for work in works:
        heapq.heappush(save, (-work, work))
    while count != n:
        tmp = heapq.heappop(save)[1]
        heapq.heappush(save, (-(tmp-1), tmp-1))
        count += 1
    for i in range(len(save)):
        if save[i][1] > 0:
            answer += pow(save[i][1], 2)
    return answer