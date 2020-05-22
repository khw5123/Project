def solution(n, from_, by, to):
    global answer
    if n == 1:
        answer.append([from_, to])
    else:
        solution(n-1, from_, to, by)
        answer.append([from_, to])
        solution(n-1, by, from_, to)

n = int(input())
answer = []
solution(n, 1, 2, 3)
print(len(answer))
for v in answer:
    print(v[0], v[1])