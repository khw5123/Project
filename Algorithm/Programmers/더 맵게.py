import heapq

def solution(scoville, K):
    answer = 0
    scoville.sort()
    while True:
        r1, r2 = heapq.heappop(scoville), heapq.heappop(scoville)
        heapq.heappush(scoville, r1 + r2*2)
        answer += 1
        if scoville[0] >= K:
            break
        if len(scoville) == 1:
            answer = -1
            break
    return answer