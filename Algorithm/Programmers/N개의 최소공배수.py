def gcd(a, b):
    a, b = int(a) if int(a) > int(b) else int(b), int(a) if int(a) < int(b) else int(b)
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return int(int(a) * int(b) / gcd(a, b))

def solution(arr):
    answer = 0
    while len(arr) != 1:
        arr.append(lcm(arr[0], arr[1]))
        del arr[0]
        del arr[0]
    answer = arr[0]
    return answer