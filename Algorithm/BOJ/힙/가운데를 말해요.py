import sys
import heapq
input = sys.stdin.readline

_max, _min = [], []
for _ in range(int(input())):
    num = int(input())
    if len(_max) == len(_min):
        heapq.heappush(_max, (-num, num))
    else:
        heapq.heappush(_min, num)
    if _max and _min:
        max_num = heapq.heappop(_max)[1]
        min_num = heapq.heappop(_min)
        if max_num > min_num:
            heapq.heappush(_max, (-min_num, min_num))
            heapq.heappush(_min, max_num)
        else:
            heapq.heappush(_max, (-max_num, max_num))
            heapq.heappush(_min, min_num)
    mid = heapq.heappop(_max)[1]
    heapq.heappush(_max, (-mid, mid))
    print(mid)