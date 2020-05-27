n = int(input())
p = sorted(list(map(int, input().split())))
answer = 0
for i in range(n):
    for j in range(i+1):
        answer += p[j]
print(answer)