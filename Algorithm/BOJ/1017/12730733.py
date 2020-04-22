'''
def dfs(x, a, d, c):
    for i in range(len(a[x])):
        t = a[x][i]
        if c[t] == True:
            continue
        c[t] = True
        if d[t] == 0 or dfs(d[t], a, d, c):
            d[t] = x
            return True
    return False

MAX = 101
d = [0] * MAX
c = [False] * MAX
a = [[], [1, 2, 3], [1], [2]]
n = len(a)
count = 0
for i in range(1, n):
    c = [False] * MAX
    if dfs(i, a, d, c):
        print(d)
        count += 1
print(count)
for i in range(1, MAX):
    if d[i] != 0:
        print("%d -> %d" % (d[i], i))
'''

import copy

def eratosthenesSieve(n):
    arr = [False, False] + [True] * (n - 1)
    primeNumber = []
    for i in range(2, n + 1):
        if arr[i] == True:
            primeNumber.append(i)
            for j in range(2 * i, n + 1, i):
                arr[j] = False
    return primeNumber

def dfs(x, a, d, c):
    for i in range(len(a[x])):
        t = a[x][i]
        if c[t] == True:
            continue
        c[t] = True
        if d[t] == 0 or dfs(d[t], a, d, c):
            d[t] = x
            return True
    return False
'''
import random
save = [random.randint(1, 1000) for _ in range(20)]
print(save)
'''
input();save = list(map(int, input().split()))
odd, even, arr, result = [], [], [], []
primeNumber = eratosthenesSieve(2000)
for num in save:
    if num % 2 == 0:
        even.append(num)
    else:
        odd.append(num)
for i in range(len(odd)):
    for j in range(len(even)):
        if save[0] % 2 == 0:
            arr.append([even[j], odd[i]])
        else:
            arr.append([odd[i], even[j]])
tmp = copy.deepcopy(arr)
for i in range(len(arr)):
    if arr[i][0] + arr[i][1] not in primeNumber:
        tmp.remove(arr[i])
arr = copy.deepcopy(tmp)
guess = []
for i in range(len(arr)):
    if save[0] in arr[i]:
        guess.append(arr[i])
for i in range(len(guess)):
    tmp = []
    for j in range(len(arr)):
        if guess[i][0] not in arr[j] and guess[i][1] not in arr[j]:
            tmp.append(arr[j])
    oddList = []
    for j in range(len(tmp)):
        if tmp[j][0] not in oddList:
            oddList.append(tmp[j][0])
    a = [[]]
    for j in range(len(oddList)):
        a.append([oddList[j]])
    evenList = []
    for j in range(len(tmp)):
        if tmp[j][1] not in evenList:
            evenList.append(tmp[j][1])
    for j in range(1, len(a)):
        for k in range(len(tmp)):
            if a[j][0] == tmp[k][0]:
                a[j].append(evenList.index(tmp[k][1]) + 1)
    for j in range(1, len(a)):
        del a[j][0]
    MAX = 51
    d = [0] * MAX
    count = 0
    for j in range(1, len(a)):
        c = [False] * MAX
        if dfs(j, a, d, c):
            count += 1
    '''
    print("------------\n%d\n%d -> %d" % (count + 1, guess[i][0], guess[i][1]))
    for j in range(1, MAX):
        if d[j] != 0:
            print("%d -> %d" % (oddList[d[j] - 1], evenList[j - 1]))
    '''
    if count == (len(odd) + len(even) - 2) // 2:
        result.append(guess[i][1])
result.sort()
if len(result) == 0:
    print(-1)
else:
    for num in result:
        print(num, end=' ')