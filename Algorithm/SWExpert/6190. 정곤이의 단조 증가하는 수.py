for t in range(int(input())):
    n = int(input())
    arr = list(map(int, input().split()))
    answer = -1
    for i in range(n):
        for j in range(n):
            if i != j:
                value = arr[i] * arr[j]
                if answer < value:
                    confirm = True
                    tmp = value
                    last = tmp % 10
                    tmp //= 10
                    while tmp != 0:
                        if tmp % 10 > last:
                            confirm = False
                            break
                        last = tmp % 10
                        tmp //= 10
                    if confirm:
                        answer = value
    print('#' + str(t+1) + ' ' + str(answer))