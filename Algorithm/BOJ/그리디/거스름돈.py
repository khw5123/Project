money = 1000-int(input())
change = [500, 100, 50, 10, 5, 1]
answer = 0
for i in range(len(change)):
    while money-change[i] >= 0:
        money -= change[i]
        answer += 1
print(answer)