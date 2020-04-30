for t in range(int(input())):
    n = int(input())
    card = list(map(str, input().split()))
    answer = ''
    if len(card) % 2 == 0:
        for i in range(len(card)//2):
            answer += (card[i] + ' ' + card[len(card)//2 + i] + ' ')
    else:
        for i in range(len(card)//2):
            answer += (card[i] + ' ' + card[len(card)//2 + i + 1] + ' ')
        answer += card[len(card)//2]
    print('#' + str(t+1), answer)