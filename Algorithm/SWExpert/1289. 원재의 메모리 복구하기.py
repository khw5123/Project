for t in range(int(input())):
    m = input()
    answer = 0 if m[0] == '0' else 1
    tmp = m[0]
    for i in range(1, len(m)):
        if tmp != m[i]:
            tmp = m[i]
            answer += 1
    print('#' + str(t+1), str(answer))