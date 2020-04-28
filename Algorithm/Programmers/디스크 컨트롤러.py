import heapq

def solution(jobs):
    answer = 0
    start, end = -1, 0
    wait = list()
    count, n = 0, len(jobs)
    while count < n:
        for job in jobs:
            if start < job[0] and job[0] <= end:
                answer += (end - job[0])
                heapq.heappush(wait, job[1])
        if len(wait):
            answer += (len(wait) * wait[0])
            start = end
            end += heapq.heappop(wait)
            count += 1
        else:
            end += 1
    answer //= n
    return answer