def solution(n, prices):
    answer, price = 0, []
    for i in range(len(prices)):
        price.append([prices[i][0]/6, prices[i][1], prices[i][0]])
    price.sort()
    while True:
        count = 6
        if n < 6:
            count = n
        sub_price = 987654321
        for i in range(len(price)):
            if price[i][1]*count > price[i][2]:
                if sub_price > price[i][2]:
                    sub_price = price[i][2]
            else:   
                if sub_price > price[i][1]*count:
                    sub_price = price[i][1]*count
        if count == 6:
            answer += sub_price*(n//count)
            n -= count*(n//count)
        else:
            answer += sub_price
            break
    return answer

n, m = map(int, input().split())
prices = []
for _ in range(m):
    prices.append(list(map(int, input().split())))
print(solution(n, prices))