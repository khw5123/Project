import itertools

for t in range(int(input())):
    n = list(map(int, input().split()))
    answer = []
    for li in list(itertools.combinations(n, 3)):
        if sum(li) not in answer:
            answer.append(sum(li))
    answer.sort(reverse=True)
    print('#' + str(t+1), str(answer[4]))