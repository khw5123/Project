n, k = map(int, input().split())
coin = []
answer = 0
for _ in range(n):
    coin.append(int(input()))
coin.sort(reverse=True)
for i in range(n):
    if k >= coin[i]:
        answer += (k//coin[i])
        k -= ((k//coin[i])*coin[i])
        if k == 0:
            break
print(answer)