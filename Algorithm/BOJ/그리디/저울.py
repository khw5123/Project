def solution(n, weight):
    answer = 1
    weight.sort()
    for i in range(n):
        if answer < weight[i]:
            break
        answer += weight[i]
    return answer

n = int(input())
weight = list(map(int, input().split()))
print(solution(n, weight))