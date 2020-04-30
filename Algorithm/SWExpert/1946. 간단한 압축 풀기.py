for t in range(int(input())):
    answer = ''
    for _ in range(int(input())):
        c, n = map(str, input().split())
        answer += (c * int(n))
    print('#' + str(t+1))
    for i in range(len(answer)):
        if i != 0 and i % 10 == 0:
            print()
        print(answer[i], end='')
    print()