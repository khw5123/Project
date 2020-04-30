for t in range(int(input())):
    a, b = map(int, input().split())
    result = [0]*10
    pos = 1
    while a <= b:
        while a % 10 != 0 and a <= b:
            for v in str(a):
                result[int(v)] += pos
            a += 1
        if a > b:
            break
        while b % 10 != 9 and a <= b:
            for v in str(b):
                result[int(v)] += pos
            b -= 1
        for i in range(10):
            result[i] += (pos*(b//10 - a//10 + 1))
        pos *= 10
        a //= 10
        b //= 10
    answer = sum([i*result[i] for i in range(len(result))])
    print('#' + str(t+1), str(answer))