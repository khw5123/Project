for t in range(int(input())):
    m1, d1, m2, d2 = map(int, input().split())
    last = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    answer = 0
    if m1 != m2:
        for i in range(m1+1, m2):
            answer += last[i-1]
        answer += (last[m1-1] - d1 + d2 + 1)
    else:
        answer = d2 - d1 + 1
    print('#' + str(t+1) + ' ' + str(answer))