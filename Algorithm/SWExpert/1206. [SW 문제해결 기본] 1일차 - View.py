for t in range(10):
    n = int(input())
    height = list(map(int, input().split()))
    answer = 0
    for i in range(2, len(height)-2):
        result = height[i] - max(height[i-2], max(height[i-1], max(height[i+1], height[i+2])))
        if result > 0:
            answer += result
    print('#' + str(t+1), str(answer))