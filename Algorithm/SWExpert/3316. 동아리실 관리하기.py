for t in range(int(input())):
    s = input()
    answer, save = [0]*16, [0]*16
    answer[1] = 1
    for i in range(len(s)):
        for j in range(1, 16):
            save[j] = answer[j]
        answer = [0]*16
        for j in range(1, 16):
            for k in range(1, 16):
                if k & (1 << (ord(s[i]) - ord('A'))) and j & k:
                    answer[k] += save[j]
                    answer[k] %= 1000000007
    print('#' + str(t+1), str(sum(answer) % 1000000007))