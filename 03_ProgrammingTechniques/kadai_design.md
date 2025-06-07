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
- 課題の条件を満たすこと

### Non-Goals

- 一般的な不正な入力への対応（例：`3 ++ 3. - 4` など構文的に誤った入力）

  - 入力の構文チェックやエラーメッセージの詳細な出力は、本実装の対象外とする。
  - 例外処理は限定的に行い、明らかなゼロ除算などにのみ対応する。
- 単項演算子や複雑な構文解析の一般対応

  - ただし、**`2 * -3` や `4 / -2` のような「乗除算における右側の負の数」**については、カッコなしでも正しく評価できるよう対応済み。

---

## 4. 提案する設計（Proposed Design）

読み取った式は、`1.0 + 2.1 - 3`の場合

```(python)
tokens = 
[{'type': 'NUMBER', 'number': 1.0}, 
{'type': 'PLUS'}, 
{'type': 'NUMBER', 'number': 2.1},
{'type': 'MINUS'}, 
{'type': 'NUMBER', 'number': 3}]
```

となるように、`tokens`という配列に各要素の型(`type`と `number`)が、格納されている

### 課題1

足し算(`PLUS`)引き算(`MINUS`)と同様に、掛け算(`MULT`)と割り算(`DIV`)を読み取る関数を追加。

また、積と商を求めて `tokens`に格納する `evaluate_multiplication_divide`関数を作成した。

#### `evaluate_multiplication_divide`関数

- `index`を `tokens`の長さ
- `x`、`+ or /`、`y`の順にデータが格納されている
- `x`、`+ or /`、`y`をそれぞれの計算結果へ変更
- `index`を-2する()
  このアルゴリズムのイメージ図を以下に示す。

<div align="center">
<img src="Image/mult_func.png" alt="mult_func" width="250"/>
</div>

### 課題2

テストケースを以下のように追加した。

```(python)
test("4-2*3+1+1/2") # 掛け算割り算
test("-3*(-2)*4*1") # 何回もかけたり割ったりする
test("2/0")   # 0で割る
```

課題3の後に追加したテストケースは以下である。

```(python)
test("(2+3)*(4-6)") # 括弧の実装
test("((3+4)*(6+1))*((5.2-3.4)*(24/(2*3)))")    # 括弧が複数回存在するとき
```

課題4の後に追加したテストケースは以下である。
'''(python)
test("abs(int(-2.34)*(-1))+round(2.34*abs(int(-45/4)))")    # 全部入れ子構造のとき
test("abs(2-3)+round(234.342)/int(-342)")  # 全関数を用いる

'''


### 課題3

左括弧が見つかったら、`evaluate_inside_bracket`関数を用いて、左括弧がある `index`を渡し、`tokens`内に括弧がない状態となるまで計算するようにした。

<div align="center">
  <img src="Image/bracket_recursive.png" alt="mult_func" width="600"/>
</div>

#### `evaluate_inside_bracket`関数 ( 引数 : 左括弧の `index`)

1. 右括弧が見つかるまで、左括弧の次の文字から一文字ずつ探索していく
2. もし左括弧が見つかれば、そのときの `index`を `evaluate_inside_bracket`関数へ渡す
3. そうでなければ、探索した `tokens[index]`を `bracket_tokens`配列内に保存
4. 右括弧が見つかったら、`bracket_tokens`内を計算し、括弧内全てを置き換える

### 課題4

`func_name`という関数が見つかったとき、``type`:`func`,`name`:`func_name``というトークンを作成する。

次に、`evaluate_func`関数を作成し、関数内の処理を行ったあと、`token`に答えをいれて返すようにした。

#### `evaluate_func`関数 ( 引数 : 関数の `index`)

1. もし関数が見つかれば、そのときの `index`を `evaluate_func`関数へ渡す
2. 前のトークンが関数でなくて、今のトークンが左括弧だったとき、課題3で作成した式に格納する
3. そうでなければ、探索した `tokens[index]`を `func_tokens`配列内に保存
4. 右括弧が見つかったら、`func_tokens`内を計算し、括弧内全てを置き換える

## 5. 代替案の検討（Alternatives Considered）

## 6. Open Questions
