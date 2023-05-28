import sys
import json
from itertools import combinations

INF = sys.maxsize

def tsp_dp(graph, start):
    n = len(graph)
    # 도시의 개수를 n이라고 가정합니다.

    # dp 배열 초기화
    dp = [[INF] * (1 << n) for _ in range(n)]
    # dp[i][j]: 현재 도시가 i이고, 방문한 도시 집합이 j일 때의 최단 경로 길이

    # 시작 도시에서 출발하는 경우를 초기화합니다.
    for i in range(n):
        if i != start:
            dp[i][1 << start | 1 << i] = graph[start][i]

    # 동적 계획법을 사용하여 최단 경로를 찾습니다.
    for r in range(3, n + 1):
        subsets = combinations(range(1, n), r-1)
        for subset in subsets:
            subset = (1 << start) | sum([1 << j for j in subset])
            for next_node in range(n):
                if next_node != start and (subset >> next_node) & 1:
                    for last_node in range(n):
                        if last_node != start and last_node != next_node and (subset >> last_node) & 1:
                            if dp[next_node][subset] is None or dp[next_node][subset] > dp[last_node][subset ^ (1 << next_node)] + graph[last_node][next_node]:
                                dp[next_node][subset] = dp[last_node][subset ^ (1 << next_node)] + graph[last_node][next_node]

    # 최단 경로 길이와 도시 방문 순서를 찾습니다.
    path = [start]
    visited = [False] * n
    visited[start] = True
    last_node = start
    length = 0

    for i in range(n - 1):
        next_node = -1
        for j in range(n):
            if j != start and not visited[j] and (1 << j | 1 << last_node) < (1 << n):
                if next_node == -1 or dp[next_node][1 << start | 1 << next_node] + graph[next_node][last_node] > dp[j][1 << start | 1 << j] + graph[j][last_node]:
                    next_node = j
        path.append(next_node)
        visited[next_node] = True
        length += graph[last_node][next_node]
        last_node = next_node

    path.append(start)
    length += graph[last_node][start]

    return length, path

with open("graph.json", "r") as f:
    graph = json.load(f)["product"]

start_city = 0
shortest_length, shortest_path = tsp_dp(graph, start_city)
location = ["중흥아파트정류장", "두끼", "심석고등학교", "호담호두과자", "메가커피", "임수오돈까스"]

print("최적 비용:", shortest_length)
print("도시 방문 순서:", [location[x] for x in shortest_path])