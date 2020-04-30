for t in range(int(input())):
    n = int(input())
    answer = set()
    count = 1
    while len(answer) != 10:
        for c in str(n*count):
            answer.add(c)
        count += 1
    print('#' + str(t+1) + ' ' + str(n*(count-1)))