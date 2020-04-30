for t in range(int(input())):
    n = int(input())
    k = int(input())
    li = sorted(list(set(map(int, input().split()))))
    answer = 0
    if k < len(li):
        distance, split = [], []
        for i in range(len(li)-1):
            distance.append(li[i+1] - li[i])
        if k != 1:
            for _ in range(k-1):
                split.append(distance.index(max(distance)))
                distance[distance.index(max(distance))] = -1
            for i in range(len(split)):
                if i == 0:
                    answer += (li[split[i]] - li[0])
                else:
                    answer += (li[split[i]] - li[split[i-1]+1])
                if i == len(split)-1:
                    answer += (li[-1] - li[split[i]+1])
        else:
            answer = li[-1] - li[0]
    print('#' + str(t+1), str(answer))