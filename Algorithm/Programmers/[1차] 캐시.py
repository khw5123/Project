def solution(cacheSize, cities):
    answer = 0
    if cacheSize == 0:
        answer = len(cities) * 5
    else:
        cache, refer = ['' for _ in range(cacheSize)], []
        for city in cities:
            if len(refer) == 0:
                cache[0] = city.lower()
                refer.append(0)
                answer += 5
            elif max(refer) < cacheSize - 1:
                if city.lower() not in cache:
                    cache[max(refer)+1] = city.lower()
                    refer.append(max(refer)+1)
                    answer += 5
                else:
                    refer.append(cache.index(city.lower()))
                    answer += 1
            else:
                if city.lower() not in cache:
                    idx = 0
                    all_, tmp = set([i for i in range(cacheSize)]), set()
                    for i in range(len(refer)-1, -1, -1):
                        tmp.add(refer[i])
                        if len(all_ - tmp) == 1:
                           idx = list(all_ - tmp)[0]
                           del refer[:i]
                           break
                    cache[idx] = city.lower()
                    refer.append(cache.index(city.lower()))
                    answer += 5
                else:
                    refer.append(cache.index(city.lower()))
                    answer += 1
    return answer