for _ in range(10):
    n = int(input())
    target = input()
    string = input()
    answer = 0
    for i in range(len(string)-len(target)+1):
        if string[i:i+len(target)] == target:
            answer += 1
    print('#' + str(n), str(answer))