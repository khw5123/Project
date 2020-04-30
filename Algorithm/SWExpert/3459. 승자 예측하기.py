depth_max, sum_ = 0, 0
for i in range(100):
    depth_max += 1
    sum_ += pow(2, i)
    if pow(10, 18) < sum_:
        break

depth_range = [[1, 1]]
for i in range(2, depth_max+1):
    depth_range.append([depth_range[-1][-1]+1])
    depth_range[-1].append(pow(2, i)-1)

for t in range(int(input())):
    n = int(input())
    answer = ''
    depth = 0
    for i in range(len(depth_range)):
        if depth_range[i][0] <= n and n <= depth_range[i][1]:
            depth = i
            break
    if depth == 0:
        answer = 'Bob'
    elif depth % 2 == 1:
        num = 2
        for i in range(depth-1):
            if i % 2 == 0:
                num = num*2 + 1
            else:
                num *= 2
        if num <= n:
            answer = 'Alice'
        else:
            answer = 'Bob'
    elif depth % 2 == 0:
        num = 3
        for i in range(depth-1):
            if i % 2 == 0:
                num *= 2
            else:
                num = num*2 + 1
        if num <= n:
            answer = 'Bob'
        else:
            answer = 'Alice'
    print('#' + str(t+1), answer)