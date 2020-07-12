from itertools import permutations

n, m = map(int, input().split())
arr = list(map(int, input().split()))
answer = set()
for sequence in permutations(arr, m):
    answer.add(sequence)
for sequence in sorted(list(answer)):
    for v in sequence:
        print(v, end=' ')
    print()