n, k = map(int, input().split())
coin = []
answer, count = 0, 0
for _ in range(n):
    coin.append(int(input()))
coin.sort(reverse=True)
for i in range(n):
    if k > coin[i]:
        while k > answer:
            answer += coin[i]
            count += 1
        if k == answer:
            break
        answer -= coin[i]
        count -= 1
print(count)