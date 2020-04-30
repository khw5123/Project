answer = []

for t in range(int(input())):
    n = int(input())
    while len(str(n)) != 1:
        n = sum(list(map(int, list(str(n)))))
    answer.append(n)

for i in range(len(answer)):
    print('#' + str(i+1), str(answer[i]))