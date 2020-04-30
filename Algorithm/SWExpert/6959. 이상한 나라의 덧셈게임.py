for t in range(int(input())):
    n = input()
    answer = 0
    while len(n) != 1:
        n = str(int(n[0]) + int(n[1])) + n[2:]
        answer += 1
    if answer % 2 == 1:
        print('#' + str(t+1) + ' A')
    else:
        print('#' + str(t+1) + ' B')