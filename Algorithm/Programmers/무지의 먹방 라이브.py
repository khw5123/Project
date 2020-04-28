from queue import PriorityQueue

def solution(food_times, k):
    answer = 0
    if sum(food_times) <= k:
        answer = -1
    else:
        sum_, prev = 0, 0
        pq = PriorityQueue()
        for i in range(len(food_times)):
            pq.put((food_times[i], i + 1))
        while sum_ + ((pq.queue[0][0] - prev) * len(pq.queue)) <= k:
            food_time = pq.get()[0]
            sum_ += (food_time - prev) * (len(pq.queue) + 1)
            prev = food_time
        pq.queue.sort(key=lambda x: x[1])
        answer = pq.queue[(k - sum_) % len(pq.queue)][1]
    return answer