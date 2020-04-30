for t in range(int(input())):
    n, k = map(int, input().split())
    li = list()
    grade = [['A+'], ['A0'], ['A-'], ['B+'], ['B0'], ['B-'], ['C+'], ['C0'], ['C-'], ['D0']]
    idx = -1
    for i in range(n):
        if i % (n // 10) == 0:
            idx += 1
        grade[idx].append(i+1)
    for i in range(n):
        a, b, c = map(int, input().split())
        li.append([a * 0.35 + b * 0.45 + c * 0.2, i+1])
    li.sort(reverse=True)
    for i in range(n):
        if li[i][1] == k:
            idx = 0
            for j in range(len(grade)):
                if i+1 in grade[j]:
                    idx = j
                    break
            print('#' + str(t+1) + ' ' + grade[idx][0])
            break