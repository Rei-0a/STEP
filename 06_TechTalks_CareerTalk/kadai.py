import sys
import math
import csv
import re
from common import print_tour, read_input
import random
import matplotlib.pyplot as plt

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calculate_distance_matrix(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]  # 全てのノード間の距離を格納する配列。N*N。
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist

def solve_greedy(cities, dist):
    N = len(cities)

    current_city = 0
    unvisited_cities = set(range(1, N)) # 訪れていない場所を格納するset
    tour = [current_city]   # 最初の場所を入れる

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    return tour

def solve_2opt(cities, tour, dist):
    # 2-opt
    #   A     B         \   A -----→ B
    #     \ /   ↖  ----- \             ↘
    #      /     X        〉            X 
    #     ↙ ↘   ↗  ----- /             ↙
    #   C     D         /   C ←----- D
    # [A,D,X,B,C] ===> [A,B,Xの逆,D,C]
    N = len(cities)
    
    changed = False
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
                        tour[a_index+1:b_index+1] = tour[a_index+1:b_index+1][::-1]
                        changed = True
                        # break
        if changed == False:
            break
    return tour

def calculate_tour_length(tour, dist):
    total_length = 0
    for i in range(len(tour)):
        from_city = tour[i]
        to_city = tour[(i + 1) % len(tour)]  # 閉路になるように
        total_length += dist[from_city][to_city]
    return total_length


# 重みづけ行列の初期化
def initialize_weight_matrix(tour):
    N = len(tour)
    weight_matrix = [[1.0]*N for i in range(N)]
    boost_weight = 3.0
    for i in range(N):
        node_from, node_to = tour[i],tour[(i+1)%N]
        weight_matrix[node_from][node_to] += boost_weight
        weight_matrix[node_to][node_from] += boost_weight

    return weight_matrix

# 蟻コロニー最適化
def solve_ant_colony(cities, tour, dist):
    # 適当に設定する必要のある変数

    alpha = 1.8 # 重みづけの優先度
    beta = 3  # ヒューリスティックの優先度
    evapotarion_rate = 0.98  # 1周ごとに重みが残る割合
    agent_num = 2000 # エージェント(蟻)の数
    boost_weight = len(cities)*10
    MIN_WEIGHT = 1e-5
    MAX_WEIGHT = 10

    length_history = [] # グラフのための、距離の履歴保存


    N = len(cities)
    best_tour = tour    # 最も良いツアーを保存する変数
    best_length = calculate_tour_length(tour,dist)   #　最も良いツアーの総距離を保存する変数
    weight_matrix = initialize_weight_matrix(tour)    # 初期の重みづけを分布

    for agent in range(agent_num):  # 各エージェントを動かす
        unvisited_cities  = set(range(0,N))  # 訪れていない都市のセット
        current_city = random.randint(0,N-1)    # 最初の探索開始地をランダムに選択
        unvisited_cities.remove(current_city)   # 最初の地点を取り除く
        current_tour = [current_city]

        while unvisited_cities: # 訪れていない都市がなくなるまで繰り返す
            cities_list = list(unvisited_cities)

            # まだ訪れていない都市それぞれへ行く確率を計算する
            bunbo = 0
            for next_city in cities_list:
                bunbo += (weight_matrix[current_city][next_city]**alpha)*((1.0/dist[current_city][next_city])**beta)# 現在の都市から次の都市までの評価値の総和
            
            probabilities = []
            for next_city in cities_list:
                # print("weight",weight_matrix[current_city][next_city]**alpha)
                # print("1.0/dist",(1.0/dist[current_city][next_city])**beta)
                probabilities.append((weight_matrix[current_city][next_city]**alpha)*((1.0/dist[current_city][next_city])**beta) /bunbo)

            # print("確率\n",probabilities)
            # 上記で求めた確率に沿って、次にどの都市に行くかを決める
            next_city = random.choices(cities_list,weights = probabilities ,k=1)[0]
            current_tour.append(next_city)  # ツアーに次の都市を追加
            unvisited_cities.remove(next_city)  # set からも取り除く
            # print("next->",next_city)
            current_city = next_city
        
        current_length = calculate_tour_length(current_tour,dist)
        # かかった距離に合わせて、重みづけを追加する
        for i in range(N):  # 今までの重みをevaporation_rate倍して、減少させる
            for j in range(N):
                weight_matrix[i][j] *= evapotarion_rate
                weight_matrix[i][j] = max(min(weight_matrix[i][j],MAX_WEIGHT),MIN_WEIGHT)
        boost_distribution = boost_weight / current_length # ゴールまでかかった距離が短いほど高いウエイトがもらえる
        # if current_length <= best_length * 1.05: # 重みの増加を、現在の解が、最適解の105%以内のときだけにする
        if current_length > 0:
            for i in range(N):  # 今通ったルートの重みを付ける
                node_from = current_tour[i]
                node_to = current_tour[(i+1)%N]
                weight_matrix[node_from][node_to] += boost_distribution
                weight_matrix[node_to][node_from] += boost_distribution
                # print(boost_distribution)
                weight_matrix[node_from][node_to] = min(weight_matrix[node_from][node_to],MAX_WEIGHT)
                weight_matrix[node_to][node_from] = min(weight_matrix[node_to][node_from],MAX_WEIGHT)
        # print(agent, current_length)
        if current_length < best_length:
            best_tour = current_tour
            best_length = current_length
            print("更新",current_length)
            for i in range(N):  # 今通ったルートの重みを付ける
                boost_distribution = (boost_weight/current_length)*2
                node_from = current_tour[i]
                node_to = current_tour[(i+1)%N]
                weight_matrix[node_from][node_to] += boost_distribution
                weight_matrix[node_to][node_from] += boost_distribution
                weight_matrix[node_from][node_to] = min(weight_matrix[node_from][node_to],MAX_WEIGHT)
                weight_matrix[node_to][node_from] = min(weight_matrix[node_to][node_from],MAX_WEIGHT)
        length_history.append(current_length)
    
    
    # 距離の収束グラフを表示
    plt.figure(figsize=(10, 5))
    plt.plot(length_history, label='Tour length')
    plt.xlabel('Iteration')
    plt.ylabel('Total Distance')
    plt.title('Ant Colony Optimization Convergence')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('aco_convergence.png')  # 画像として保存
    plt.show()


    # print(tour)
    # length = calculate_tour_length(tour,dist)
    # print("current ", length)
    return best_tour



def solve(cities):
    dist = calculate_distance_matrix(cities)
    tour = solve_greedy(cities,dist)
    tour = solve_2opt(cities, tour, dist)
    
    print("greedy+2opt",calculate_tour_length(tour,dist))
    tour = solve_ant_colony(cities,tour, dist)
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    # print_tour(tour)
    print("finished")
    with open('output_4.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index'])
        for city in tour:
            writer.writerow([city])
