from math import factorial

for t in range(int(input())):
    a, b = map(int, input().split())
    a, b = a/100, b/100
    probability_a, probability_b = 0., 0.
    for count in [2, 3, 5, 7, 11, 13, 17]:
        # 소수개의 완제품을 만들 확률 = 만들 수 있는 최대 완제품 18개 중 소수개의 완제품을 선택하는 경우의 수 * 만들 수 있는 최대 완제품 18개 중 소수개의 완제품을 만들 확률
        probability_a += ((factorial(18)/(factorial(count)*factorial(18-count))) * (pow(a, count)*(pow(1-a, 18-count))))
        probability_b += ((factorial(18)/(factorial(count)*factorial(18-count))) * (pow(b, count)*(pow(1-b, 18-count))))
    # A, B 중 한 명이라도 소수개의 완제품을 만들 확률 = 1 - (A, B 모두 소수개의 완제품을 만들지 못할 확률 == ((1 - A가 소수개의 완제품을 만들 확률) * (1 - B가 소수개의 완제품을 만들 확률)))
    answer = 1 - ((1-probability_a) * (1-probability_b))
    print('#' + str(t+1), '%.6f' % round(answer, 6))