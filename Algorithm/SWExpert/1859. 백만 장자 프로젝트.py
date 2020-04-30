for t in range(int(input())):
    n = int(input())
    price = list(map(int, input().split()))
    base, answer = n-1, 0
    for i in range(n-2, -1, -1):
        if price[i] < price[base]:
            answer += (price[base] - price[i])
        else:
            base = i
    print('#' + str(t+1) + ' ' + str(answer))