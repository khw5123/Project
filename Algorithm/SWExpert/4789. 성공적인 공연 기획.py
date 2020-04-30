for t in range(int(input())):
    n = input()
    answer, current = 0, 0
    for i in range(len(n)):
        if int(n[i]) != 0:
            if current >= i:
                current += int(n[i])
            else:
                answer += (i - current)
                current = i + int(n[i])
    print('#' + str(t+1), str(answer))