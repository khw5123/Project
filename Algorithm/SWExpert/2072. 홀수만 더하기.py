for i in range(int(input())):
    sum_ = 0
    for n in list(map(int, input().split())):
        if n % 2 == 1:
            sum_ += n
    print('#' + str(i+1) + ' ' + str(sum_))