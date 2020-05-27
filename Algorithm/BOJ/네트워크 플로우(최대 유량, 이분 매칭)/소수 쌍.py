def sieveOfEratosthenes(n):
    sieve = [True]*n
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*2, n, i):
                sieve[j] = False
    return [i for i in range(2, n) if sieve[i]]

def dfs(nNode, n, m, num, match, nMatch, mMatch, visit):
    if visit[nNode]:
        return False
    visit[nNode] = True
    for mNode in match[nNode]:
        if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, m, num, match, nMatch, mMatch, visit):
            nMatch[nNode], mMatch[mNode] = mNode, nNode
            return True
    return False

def bipartiteMatch(n, m, num, match):
    answer = []
    for first in match[1]: # 첫 번째 수와 매칭가능한 경우만큼 반복
        nMatch, mMatch = [-1]*(n+1), [-1]*(m+1)
        for nNode in range(2, n+1): # 첫 번째 수는 매칭되었다고 가정해야하므로 두 번째 수 부터 매칭 시작
            visit = [False]*(n+1)
            nMatch[1], mMatch[first], visit[1] = first, 1, True # 첫 번째 수는 매칭되었다고 설정
            dfs(nNode, n, m, num, match, nMatch, mMatch, visit) # n번째 수 매칭
        confirm = True # 모든 수의 매칭 여부
        for v in nMatch[1:]:
            if v == -1:
                confirm = False
                break
        if confirm:
            answer.append(num[first-1])
    answer.sort()
    return answer

n = int(input())
num = list(map(int, input().split())) # 수 리스트
match = [[] for _ in range(n+1)]
prime = sieveOfEratosthenes(2000) # 소수 리스트(최대 1000인 자연수들만 존재하고, 두 수를 합하면 최대 2000)
for _n in range(1, n+1):
    for _m in range(1, n+1):
        # 같지 않은 두 수를 더한 값이 소수일 경우에만 매칭
        if _n != _m and num[_n-1]+num[_m-1] in prime:
            match[_n].append(_m)
answer = bipartiteMatch(n, n, num, match)
if answer:
    for v in answer:
        print(v, end=' ')
    print()
else:
    print(-1)
'''
def sieveOfEratosthenes(n):
    sieve = [True]*n
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*2, n, i):
                sieve[j] = False
    return [i for i in range(2, n) if sieve[i]]

def dfs(x, a, d, c):
    for i in range(len(a[x])):
        t = a[x][i]
        if c[t]:
            continue
        c[t] = True
        if d[t] == 0 or dfs(d[t], a, d, c):
            d[t] = x
            return True
    return False

n = int(input())
num = list(map(int, input().split()))
odd, even, arr = [i for i in num if i%2 != 0], [i for i in num if i%2 == 0], []
prime = sieveOfEratosthenes(2000)
answer = []
for i in range(len(odd)):
    for j in range(len(even)):
        if odd[i]+even[j] in prime:
            if num[0]%2 == 0:
                arr.append([even[j], odd[i]])
            else:
                arr.append([odd[i], even[j]])
guess = [v for v in arr if num[0] in v]
for i in range(len(guess)):
    tmp = [v for v in arr if guess[i][0] not in v and guess[i][1] not in v]
    oddList, evenList = list(set([v[0] for v in tmp])), list(set([v[1] for v in tmp]))
    a, d, count = [[]] + [[v] for v in oddList], [0]*(n+1), 0
    for j in range(1, len(a)):
        for k in range(len(tmp)):
            if a[j][0] == tmp[k][0]:
                a[j].append(evenList.index(tmp[k][1]) + 1)
    for j in range(1, len(a)):
        del a[j][0]
    for j in range(1, len(a)):
        c = [False]*(n+1)
        if dfs(j, a, d, c):
            count += 1
    if count == (len(odd)+len(even)-2) // 2:
        answer.append(guess[i][1])
answer.sort()
if answer:
    for v in answer:
        print(v, end=' ')
    print()
else:
    print(-1)
'''