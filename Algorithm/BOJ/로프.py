def solution(n, weight):
    answer = 0
    weight.sort(reverse=True)
    for i in range(n):
        if weight[i]*(i+1) > answer:
            answer = weight[i]*(i+1)
    return answer

n = int(input())
weight = [0]*n
for i in range(n):
    weight[i] = int(input())
print(solution(n, weight))