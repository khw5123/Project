for t in range(int(input())):
    string = input()
    confirm = True
    for i in range(len(string) // 2):
        if string[i] != string[len(string)-i-1]:
            confirm = False
            break
    if confirm:
        print('#' + str(t+1) + ' 1')
    else:
        print('#' + str(t+1) + ' 0')