for t in range(int(input())):
    n = int(input())
    answer = -1
    for i in range(1, pow(10, 6)+1):
        if n == pow(i, 3):
            answer = i
            break
    print('#' + str(t+1), str(answer))