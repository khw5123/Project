for i in range(int(input())):
    a, b = map(int, input().split())
    if a > b:
        print('#' + str(i+1) + ' >')
    elif a < b:
        print('#' + str(i+1) + ' <')
    else:
        print('#' + str(i+1) + ' =')