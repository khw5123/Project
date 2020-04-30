for t in range(int(input())):
    n = int(input())
    li = [2, 3, 5, 7, 11]
    answer = [0] * len(li)
    for i in range(len(li)-1, -1, -1):
        count = 0
        while True:
            if n % li[i] == 0:
                n //= li[i]
                count += 1
            else:
                break
        answer[i] = count
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()