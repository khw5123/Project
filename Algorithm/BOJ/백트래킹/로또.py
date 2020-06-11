def solution(_set, depth):
    if len(_set) == 6:
        print(' '.join(map(str, _set)))
        return
    if depth == len(li):
        return
    solution(_set+[li[depth]], depth+1)
    solution(_set, depth+1)

while True:
    k, *li = list(map(int, input().split()))
    if k == 0:
        break
    solution([], 0)
    print()
'''
def solution(_set, depth):
    if depth == 6:
        key = ' '.join(sorted(map(str, _set)))
        if key not in answer:
            answer[key] = 1
            print(' '.join(map(str, _set)))
        return
    for i in range(depth, len(li)):
        if li[i] not in _set:
            solution(_set+[li[i]], depth+1)

while True:
    k, *li = list(map(int, input().split()))
    if k == 0:
        break
    answer = {}
    solution([], 0)
    print()
'''
'''
from itertools import combinations

while True:
    k, *li = list(map(int, input().split()))
    if k == 0:
        break
    for v in sorted(list(combinations(li, 6))):
        print(' '.join(map(str, v)))
    print()
'''