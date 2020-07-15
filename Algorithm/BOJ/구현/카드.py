import sys
input = sys.stdin.readline

n, save = int(input()), dict()
answer = [0, 0]
for _ in range(n):
    num = int(input())
    if num not in save:
        save[num] = 1
    else:
        save[num] += 1
for k, v in save.items():
    if v > answer[1]:
        answer = [k, v]
    elif v == answer[1]:
        if k < answer[0]:
            answer[0] = k
print(answer[0])