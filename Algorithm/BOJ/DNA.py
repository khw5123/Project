def solution(n, m, DNA):
    answer = ['', 0]
    save = [[] for _ in range(m)]
    for i in range(m):
        di = {}
        for j in range(n):
            if DNA[j][i] not in di:
                di[DNA[j][i]] = 1
            else:
                di[DNA[j][i]] += 1
        for k, v in di.items():
            save[i].append([v, ord(k)])
        save[i].sort(key=lambda x:(x[0], -x[1]))
    for i in range(len(save)):
        answer[0] += chr(save[i][-1][1])
    for i in range(m):
        for j in range(n):
            if answer[0][i] != DNA[j][i]:
                answer[1] += 1
    return answer

n, m = map(int, input().split())
DNA = []
for _ in range(n):
    DNA.append(input())
for v in solution(n, m, DNA):
    print(v)