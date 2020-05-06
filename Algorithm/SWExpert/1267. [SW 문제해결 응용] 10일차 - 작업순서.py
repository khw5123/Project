for t in range(10):
    v, e = map(int, input().split())
    li = [[0]*(v+1) for _ in range(v+1)]
    answer = []
    tmp = list(map(int, input().split()))
    for i in range(0, len(tmp), 2):
        li[tmp[i+1]][tmp[i]] = 1
    while len(answer) != v:
        for i in range(1, len(li)):
            if sum(li[i]) == 0 and i not in answer:
                answer.append(i)
                break
        for i in range(1, len(li)):
            li[i][answer[-1]] = 0
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()