for i in range(int(input())):
    date = input()
    li = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if int(date[4:6]) > 0 and int(date[4:6]) < 13 and int(date[6:8]) > 0 and int(date[6:8]) <= li[int(date[4:6])-1]:
        print('#' + str(i+1) + ' ' + date[:4] + '/' + date[4:6] + '/' + date[6:])
    else:
        print('#' + str(i+1) + ' -1')