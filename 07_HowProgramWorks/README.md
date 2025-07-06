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

### 4.1 Best-Fit malloc

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



## 5. 代替案の検討（Alternatives Considered）


<!-- 
## 6. Open Questions -->
