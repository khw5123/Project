for t in range(int(input())):
    n = int(input())
    price = sorted(list(map(int, input().split())), reverse=True)
    answer = sum(price)
    for i in range(2, len(price), 3):
        answer -= price[i]
    print('#' + str(t+1), str(answer))