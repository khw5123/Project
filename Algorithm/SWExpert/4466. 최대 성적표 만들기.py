for t in range(int(input())):
    n, k = map(int, input().split())
    score = sorted(list(map(int, input().split())), reverse=True)
    print('#' + str(t+1), str(sum(score[:k])))