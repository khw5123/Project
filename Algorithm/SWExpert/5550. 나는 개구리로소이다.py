for t in range(int(input())):
    s = list(input())
    answer = 0
    while len(s) != 0:
        idx = 0
        exit_ = True
        remove_ = []
        together = []
        for i in range(len(s)):
            if idx == 0 and s[i] == 'c':
                idx += 1
                remove_.append(i)
            elif idx == 1 and s[i] == 'r':
                idx += 1
                remove_.append(i)
            elif idx == 2 and s[i] == 'o':
                idx += 1
                remove_.append(i)
            elif idx == 3 and s[i] == 'a':
                idx += 1
                remove_.append(i)
            elif idx == 4 and s[i] == 'k':
                idx += 1
                remove_.append(i)
                exit_ = False
                break
            if idx != 0 and s[i] == 'c':
                together.append(i)
                answer = max(answer, len(together))
        for i in range(len(remove_)-1, -1, -1):
            del s[remove_[i]]
        if exit_:
            answer = -1
            break
    print('#' + str(t+1), str(answer))