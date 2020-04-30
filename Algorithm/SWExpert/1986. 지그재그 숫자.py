for t in range(int(input())):
    answer = 1
    for i in range(2, int(input())+1):
        if i % 2 == 0:
            answer -= i
        else:
            answer += i
    print('#' + str(t+1) + ' ' + str(answer))