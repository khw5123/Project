for t in range(int(input())):
    n = int(input())
    height = sorted(list(map(int, input().split())))
    li = [height.pop()]
    while len(height) != 0:
        li.insert(0, height.pop())
        if height:
            li.append(height.pop())
    answer = max(0, abs(li[0]-li[-1]))
    for i in range(len(li)-1):
        answer = max(answer, abs(li[i]-li[i+1]))
    print('#' + str(t+1), answer)