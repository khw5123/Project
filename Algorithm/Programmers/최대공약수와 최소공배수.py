def gcd(a, b):
    a, b = int(a) if int(a) > int(b) else int(b), int(a) if int(a) < int(b) else int(b)
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return int(int(a) * int(b) / gcd(a, b))

def solution(n, m):
    answer = []
    answer.append(gcd(n, m))
    answer.append(lcm(n, m))
    return answer