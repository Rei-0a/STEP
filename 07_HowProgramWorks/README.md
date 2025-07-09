## 1. 概要

**目的**：[malloc](https://github.com/hikalium/malloc_challenge)に対して行う一連の拡張について、それぞれの設計方針をまとめる。

---

## 2. 各課題の内容

### 課題1：Cポインタ百ます計算

授業中に配布された解答、考察を書く

### 課題2：mallocの性能を改善する

- First Fit、Best Fit、Worst Fitを実装し、その性能について考察を行う
    - simple_malloc.cの実装は[First Fit](https://github.com/hikalium/malloc_challenge)になっているので、改造する
    - First list binを実装し、考察

### 自由課題　malloc challenge✨

- 自由に改善して性能を向上させる！
    - UtilizationとSpeedが大切

### 実行方法
1. mallocディレクトリ内で、makeを実行
2. mallocディレクトリ内でmake run_traceを実行した後、[malloc visualizer](https://hikalium.github.io/malloc_challenge/visualizer/)にアクセスして、mallocの動きを観察できる🔍

<!-- ---

## 3. Goals and Non-Goals

### 目的（Goals）


### Non-Goals -->



---

## 4. 提案する設計（Proposed Design）

Best-Fit型にして、FreeListBinにした。

### 4.1 Best-Fit malloc

最後まで`metadata`を確認して、必要な`size`よりも大きい`metadata->size`を持つ中で最小の領域(適切な領域)を探す。

```
// Best-fit
  my_metadata_t *best_metadata = NULL;
  my_metadata_t *best_prev = NULL;
  while (metadata) {  // 次のmetadataがなくなるまで、bestなmetadataを探す
    if (size <= metadata->size){  // sizeよりも大きいmetadata->sizeが見つかった
      if ( best_metadata == NULL || metadata->size < best_metadata->size){ // 必要なサイズ < metadataのサイズ < 今のベストサイズ のとき
        best_metadata = metadata;
        best_prev = prev;
    }
    }
    prev = metadata;
    metadata = metadata->next;
  }
  prev = best_prev; // 最も良いmetadataにする。
  metadata = best_metadata;
```

### 4.2 Free List Bin
構造体を
```
typedef struct my_heap_t {
  my_metadata_t *free_head[N];
  my_metadata_t dummy;
} my_heap_t;
```
のように書き換えて、free_headを`N`個にした。(つまり、ビンの数を`N`個にした。)
各ビンが格納するメモリのサイズは
```C
bin_size_start[N] = {0,100,300,500,700,900,1000,1200};
```
とした。

その後、`metadata`のサイズが入る`bin`のインデックスを計算し(`caluculate_bin_index`関数)した。それ以上のインデックスを持つ`bin`を探索し、`free size list`から`bestfit`を用いて空いているメモリを探した。



### 4.2 

## 5. 結果

最初の実行結果
```
Challenge #2    |   simple_malloc =>       my_malloc
--------------- + --------------- => ---------------
       Time [ms]|              26 =>              23
Utilization [%] |              39 =>              39
====================================================
Challenge #3    |   simple_malloc =>       my_malloc
--------------- + --------------- => ---------------
       Time [ms]|             339 =>             258
Utilization [%] |               9 =>               9
====================================================
Challenge #4    |   simple_malloc =>       my_malloc
--------------- + --------------- => ---------------
       Time [ms]|           89289 =>           91900
Utilization [%] |              16 =>              16
====================================================
Challenge #5    |   simple_malloc =>       my_malloc
--------------- + --------------- => ---------------
       Time [ms]|           99037 =>           92859
Utilization [%] |              15 =>              15

Challenge done!
Please copy & paste the following data in the score sheet!
16,70,23,39,258,9,91900,16,92859,15,
```

Challenge 1
全て128
Challenge 2
ほとんど2桁のメモリを要求している
Challenge 3
同じ
Challenge 4
ほとんど3桁のメモリを要求している (4桁含む)
Challenge 4
2桁~4桁までランダムにメモリを要求している


##### (0) First Fit

##### (1) Best Fitの実装
(0)と比較して、Utilicationは全てのChallengeで改善された。これは、最小限のブロックを使うことになり、結果として、断片化が抑えられているからであると考えられる。
また、Challenge 1,2,3は実行時間が伸びたが、Challenge 4,5は実行時間が短縮された。これは、Challenge1~3は、必要なメモリが小さいため、すぐに見つけたところにいれても、他のメモリの確保にあまり影響を与えないため、実行時間が伸びたのではないかと考えられる。

##### (2) Free List Binの実装
##### ()
##### ()

## 5. 代替案の検討（Alternatives Considered）

##### Free-List-Binの各`bin`が担当するデータサイズの範囲
- (1)`int bin_size_start[N] = {0,100,300,500,700,900,1000,1200};`のとき
- (2)`int bin_size_start[N] = {0,50,100,300,500,700,900,1000,1200,1400};`のとき
`N=10`としたが、`N=8`のときよりも時間がかかってしまった。




<!-- 
## 6. Open Questions -->
