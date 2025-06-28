import sys
import math
import csv
import re
from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]  # 全てのノード間の距離を格納する配列。N*N。
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N)) # 訪れていない場所を格納するset
    tour = [current_city]   # 最初の場所を入れる

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    # 2-opt
    #   A     B         \   A -----→ B
    #     \ /   ↖  ----- \             ↘
    #      /     X        〉            X 
    #     ↙ ↘   ↗  ----- /             ↙
    #   C     D         /   C ←----- D
    # [A,D,X,B,C] ===> [A,B,Xの逆,D,C]

    while True:
        changed = False
        for a_index in range(N):  # tourのエッジをそれぞれ見ていく。a_indexは、何番目に通るエッジかを表している。
            a = tour[a_index]
            d = tour[(a_index+1)%N]
            
            for b_index in range(N):    # B -> C を全エッジ探索
                if a_index != b_index:  # A -> D と B -> C が異なるとき
                    b = tour[b_index]
                    c = tour[(b_index+1) % N]

                    if (dist[a][d] + dist[b][c]) > (dist[a][b] + dist[c][d]):   # (A->DとB->Cの長さ) > (A->BとC->Dの長さ)のとき、
                        # print(a,d,'->',b,c)
                        changed = True
                        tour[a_index+1:b_index+1] = tour[a_index+1:b_index+1][::-1]

        if changed == False:
            break

    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    with open('output_6.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index'])
        for city in tour:
            writer.writerow([city])
