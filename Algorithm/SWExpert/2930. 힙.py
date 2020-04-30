import heapq

for t in range(int(input())):
    heap, answer = [], []
    for _ in range(int(input())):
        num = list(map(int, input().split()))
        if len(num) == 2:
            heapq.heappush(heap, (-num[1], num[1]))
        else:
            if len(heap) == 0:
                answer.append(-1)
            else:
                answer.append(heapq.heappop(heap)[1])
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()