def solution(number, k):
    answer = ''
    confirm = False
    idx = 0
    while k != 0:
        if not confirm:
            confirm2 = True
            for i in range(idx, len(number)-1):
                if int(number[i]) < int(number[i+1]):
                    idx = i
                    confirm2 = False
                    break
            if confirm2:
                confirm = True
                number = number[:len(number)-1]
            else:
                number = number[:idx] + number[idx+1:]
                if idx != 0:
                    idx -= 1
        else:
            number = number[:len(number)-1]
        k -= 1
    answer = number
    return answer