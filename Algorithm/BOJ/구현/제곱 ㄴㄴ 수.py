from math import sqrt

_min, _max = map(int, input().split())
sieve, answer = [0]*1000001, _max-_min+1
for i in range(2, int(sqrt(_max))+1):
    j = (_min // pow(i, 2)) + 1 if _min % pow(i, 2) else _min // pow(i, 2)
    while pow(i, 2)*j <= _max:
        sieve[pow(i, 2)*j - _min] = 1
        j += 1
answer -= sum(sieve)
print(answer)