def solution(n):
    answer = list()
    save = ['1','2','4']
    while n > len(save):
        if n % 3 == 0:
            answer.append(save[-1])
            n //= 3
            n -= 1
        else:
            answer.append(save[(n%3)-1])
            n //= 3
    answer.append(save[(n%3)-1])
    answer.reverse()
    return ''.join(answer)