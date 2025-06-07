## 1. 概要

**目的**：[モジュール化された計算機プログラム](https://docs.google.com/document/d/1H6mhc7Dje0BTeIDAmCIy4GBOUC3Y1uKG8iq4qOq5QYs/edit?tab=t.0)に対して行う一連の拡張（課題1〜4）について、それぞれの設計方針をまとめる。

---

## 2. 各課題の内容

### 課題1：掛け算と割り算の追加

- 掛け算（`*`）と割り算（`/`）の演算を実装する。
- 不正な入力はないと仮定。
  - 「*」「/」と「+」「−」の優先度をしっかり扱うこと。

### 課題2：テストケースの追加

- 書いたプログラムが正しく動いていることを確認するためのテストケースを追加
  - できるだけ網羅的についかする

### 課題3：括弧に対応する機能の追加

- テストケースも追加すること

### 課題4(できれば)：関数の追加

- abs(), int(), round() に対応しよう
  - abs(-2.2) => 2.2 （絶対値）
  - int(1.55) => 1（小数を切捨てる）
  - round(1.55) => 2（四捨五入）

---

## 3. Goals and Non-Goals

### 目的（Goals）

- 拡張性の高いモジュール設計を行うこと
- テストケースを網羅的に実装すること

### Non-Goals

- 不正な入力への対応(ex : 3 ++ 3. - 4 )

---

## 4. 要件（Requirements）

### 機能要件（Functional Requirements）

- 入力値として〇〇を受け取り、□□を返す
- 不正な入力が与えられた場合の処理（必要に応じて）

### 非機能要件（Non-Functional Requirements）

- 時間・空間計算量は適切な範囲内（例：O(n)）
- コードの可読性と保守性を重視

---

## 5. 提案する設計（Proposed Design）

現在(足し算引き算小数の機能のみ)は、`1.0 + 2.1 - 3`の場合

```(python)
tokens = 
[{'type': 'NUMBER', 'number': 1.0}, 
{'type': 'PLUS'}, 
{'type': 'NUMBER', 'number': 2.1},
{'type': 'MINUS'}, 
{'type': 'NUMBER', 'number': 3}]
```

のように、1行読み取った後、`tokens`という配列に各要素の型(`type`と `number`)が、格納されている

### 課題1

- 足し算(`PLUS`)引き算(`MINUS`)と同様に、掛け算(`MULT`)と割り算(`DIV`)を読み取る関数を追加。
- 積と商を求めて`tokens`に格納する`evaluate_multiplication_divide`関数を作成
  - `index`を`tokens`の長さ
  - `x`、`+ or /`、`y`の順にデータが格納されている
  - `x`、`+ or /`、`y`をそれぞれの計算結果へ変更
  - `index`を-2する()
  <!-- ![alt text](Image/mult_func.png) -->

    <img src="Image/mult_func.png" alt="mult_func" width="100"/>

### 課題2

テストケースを以下のように追加した。
```
test("4-2*3+1+1/2") # 掛け算割り算
test("3*2*4*1") # 何回もかけたり割ったりする
test("2/0")   # 0で割る
```

### 課題3

### 課題4

## 5. 代替案の検討（Alternatives Considered）

## 6. Open Questions
