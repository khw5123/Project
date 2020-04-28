import heapq

def solution(stock, dates, supplies, k):
    answer = 0
    save = list()
    idx = 0
    while stock < k:
        for i in range(idx, len(dates)):
            if dates[i] <= stock:
                heapq.heappush(save, (-supplies[i], supplies[i]))
                idx = i + 1
            else:
                break
        stock += heapq.heappop(save)[1]
        answer += 1
    return answer