for t in range(int(input())):
    n = int(input())
    if n % 2 == 0:
        print('#' + str(t+1) + ' Even')
    else:
        print('#' + str(t+1) + ' Odd')