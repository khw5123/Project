def solution(a, b):
    answer = ''
    w = ['THU', 'FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED']
    d = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    n = b
    for i in range(a-1):
        n += d[i]
    answer = w[n % 7]
    return answer