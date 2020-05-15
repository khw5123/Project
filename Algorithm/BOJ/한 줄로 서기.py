def solution(n, taller):
    answer = [n]
    for i in range(n-2, -1, -1):
        if taller[i] == 0:
            answer.insert(0, i+1)
        else:
            answer.insert(taller[i], i+1)
    return answer

n = int(input())
taller = list(map(int, input().split()))
for v in solution(n, taller):
    print(v, end=' ')
print()