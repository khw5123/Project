for t in range(int(input())):
    n = int(input())
    size = []
    answer = 0
    for i in range(n):
        size.append(int(input()))
    for num in size:
        if num < sum(size)//n:
            answer += (sum(size)//n - num)
    print('#' + str(t+1), str(answer))