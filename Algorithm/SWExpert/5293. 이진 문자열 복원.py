for t in range(int(input())):
    answer = ''
    count = list(map(int, input().split()))
    if count[1] == 0 and count[2] == 0:
        if count[0] != 0 and count[3] != 0:
            answer = 'impossible'
        elif count[0] != 0:
            answer = '0' + '0'*count[0]
        elif count[3] != 0:
            answer = '1' + '1'*count[3]
    elif count[1] - count[2] == 1 or count[2] == count[1]:
        count[1] -=1
        answer = '0' + '0'*count[0] + '1' + '1'*count[3]
        for i in range(count[1] + count[2]):
            if i % 2 == 0:
                answer += '0'
            else:
                answer += '1'
    elif count[2] - count[1] == 1:
        count[2] -=1
        answer = '1' + '1'*count[3] + '0' + '0'*count[0]
        for i in range(count[1] + count[2]):
            if i % 2 == 0:
                answer += '1'
            else:
                answer += '0'
    else:
        answer = 'impossible'
    print('#' + str(t+1), answer)