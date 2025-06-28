## 1. 概要

課題5に引き続き、TSP(Traveling Salesperson Problem)について考える。

```

python -m http.server # For Python 3

python -m SimpleHTTPServer 8000 # If you don’t want to install Python 3

```

を実行した後に、[リンク](http://localhost:8000/visualizer/build/default/)を開くことでビジュアライズ可能。

## 2. 各課題の内容

TSPを実際に実装して、様々なアルゴリズムや工夫をしてみる。

[サンプルコード](https://github.com/hayatoito/google-step-tsp)を用いた。

貪欲法を用いた後に、2-opt法を用いたときの経路長([コード](https://github.com/Rei-0a/STEP/tree/main/05_TSPChallenge))よりも、短くなるようなアルゴリズムを考える。また、今回用いるデータは、都市の長さ `N`が、`N=2048`のとき、`N=8192`のときを考える。

## 3. 提案する設計

### 1 2-opt法

```(python)

     2-opt

       A     B         \   A -----→ B

         \ /   ↖  ----- \             ↘

          /     X        〉            X 

         ↙ ↘   ↗  ----- /             ↙

       C     D         /   C ←----- D

```

ルート内に、左のようなクロスが発生してしまっているとき、[A,D,X,B,C] ===> [A,B,Xの逆,D,C]のように、その紐をほどき、クロスをなくした。

1. 上記図のA->D　エッジを探索

  a. 上記図のB->C　エッジを探索

  b. A -> D とB -> C　が異なるエッジのとき

    (A->DとB->Cの長さ) > (A->BとC->Dの長さ)なら、D,X,Bの配列を、B,Xの逆順, Dの順に格納する

2.1. を、変更がなくなるまで繰り返す

### 2. 蟻コロニー最適化 🐜

貪欲法→2opt法を行ったあとの経路に重みづけをした状態で、アリコロニー最適化を行う。

1. エージェント(蟻)と重み行列の初期化を行う(貪欲法などで得た解に初期重みを追加する)
2. 各エージェントに対して以下の処理を繰り返す。
   1. (まだ通っていない)各都市に対して、重みとヒューリスティックな情報(今回は距離の逆数とした)に基づいて解の選択を行う。(*)
   2. 重みを更新する(**)
3. 最も良い成績のエージェントの解を出力する。

##### (*) 解の選択方法

今、都市 $i$にいるとする。

また、まだ訪問していない都市の集合を $Ω$とする。

このとき、各アリが現在の都市 $i$ から次の都市 $j\in\Omega$ を選択する確率 $P_{ij}$ を以下のように定義した

$$
P_{ij} = \frac{\tau_{ij}^{\alpha} \cdot \eta_{ij}^{\beta}}{\sum_{k \in \text{allowed}} \tau_{ik}^{\alpha} \cdot \eta_{ik}^{\beta}}
$$

- $\tau_{ij}$：辺 $(i, j)$ 上の重み量
- $\eta_{ij} = \frac{1}{d_{ij}}$：都市 $i$ から $j$ へのヒューリスティック情報（距離の逆数）
- $\alpha$：重みの重要度を調整するパラメータ（例：1）
- $\beta$：ヒューリスティック情報の重要度を調整するパラメータ（例：2）

  この確率に基づいて、ランダムに次の都市を選んだ。

##### (**) 重みの更新

今までの重みをある割合`evapotarion_tate`倍して、減少させた。その後、解として得たルートに、そのルートの総距離の逆数だけ重みを足しいれた。

##### 変数の設定

重みの追加を行うときを、最適値の105%以内の値にするよりも、そのままの方がよさそうであった


##### 📚 参考文献

1. ganyariya, 「【アントコロニー最適化(ACO)を救いたい」, Qiita, 2021.[https://qiita.com/ganyariya/items/25824f1502478a673005](https://qiita.com/ganyariya/items/25824f1502478a673005)
2. 田邊遼司, 「進化計算アルゴリズムの改良研究～アリコロニー最適化を例に～」, 横浜国立大学 スライド資料.
   [https://ryojitanabe.github.io/pdf/t-ynu-oa_slides.pdf](https://ryojitanabe.github.io/pdf/t-ynu-oa_slides.pdf)

## 4. 実行結果

### 1. 2-opt法を用いたとき

<!-- 1行目：4枚 -->

<palign="center">

  <imgsrc="Image/2opt_0.png"width="200"/>

  <imgsrc="Image/2opt_1.png"width="200"/>

  <imgsrc="Image/2opt_2.png"width="200"/>

  <imgsrc="Image/2opt_3.png"width="200"/>

</p>

<!-- 2行目：3枚 -->

<palign="center">

  <imgsrc="Image/2opt_4.png"width="200"/>

  <imgsrc="Image/2opt_5.png"width="200"/>

  <imgsrc="Image/2opt_6.png"width="200"/>

</p>

## 6. Open Questions

## 7. 計算量

時間：`O(E)`

空間:`O(V)`

負のコストが辺に入っていたら、ベルマンフォード法がある！

delta を0にするのは、コンピュータの整数の仕組み上、とても難しい！
