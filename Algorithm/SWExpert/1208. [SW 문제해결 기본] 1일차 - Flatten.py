for t in range(10):
    count = int(input())
    height = list(map(int, input().split()))
    while count != 0:
        height[height.index(min(height))] += 1
        height[height.index(max(height))] -= 1
        count -= 1
    print('#' + str(t+1), str(max(height) - min(height)))