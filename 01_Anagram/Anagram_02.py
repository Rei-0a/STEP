'''
与えられた文字列の全ての文字を使わなくても良いように関数をアップグレードする。
入力：small.txt , medium.txt, large.txt
出力：各単語について「最大のスコアを持つアナグラム」を列挙したファイル
単語のスコアは、文字によって点数が変わる
    onePointChar = ['a','e','h','i','n','o','r','s','t']
    twoPointChar = ['c','d','l','m','u']
    threePointChar = ['b','f','g','p','v','w','y']
    fourPointChar = ['j','k','q','x','z']

'''

import re
import sys

# テストケース
# test = 'asdgawega'  # 存在しないとき
# test = 'a ".t22'    # 文字以外が沢山ある
# test = 'cat'    # 複数のアナグラムを持つとき
# test = '  '
test = 'cAtcHlands' # 長くて大文字も含まれているとき
# test = 'a'
# test = 'zymurgy'

# 辞書ファイルの取得、1行ごとに保存
f = open('words.txt','r')
data = f.read().splitlines()    # 1行ごとにデータを取得。辞書データの\nは除去。
f.close()

# 新しい辞書(それぞれの単語のアルファベットを数えたもの、元の単語、スコア)を作成する関数
def createCountedDictionary( words ):

    countedDictionary = []    
    Point = [1,3,2,2,1,3,3,1,1,4,4,2,2,1,1,3,4,1,1,1,2,3,3,4,3,4]

    for word in words:
        alphabetsCount = [0]*26
        score = 0
        for j in range(len(word)):
            alphabetsCount[(ord(word[j])-ord('a'))] += 1    # a:0 ~ z:25 の場所をインクリメント
            score += Point[(ord(word[j])-ord('a'))]         # wordのスコアも計算しておく
        
        alphabetsCount.append(word)     # 元の単語をアペンド
        alphabetsCount.append(score)    # その単語が持つスコアをアペンド
        countedDictionary.append(alphabetsCount)
        
    countedDictionary=sorted(countedDictionary, key= lambda x: x[27], reverse=True) # 単語が持つ点数が高い順にソートする

    return countedDictionary

# アルファベットをカウントした単語(input) が、辞書(Words)の中にあるかを調べていく関数
def anagramSearch( input , Words):
    anagramSets= []
        
    for i in range(len(Words)):
        canCreate = True   # Words[i][:]が作れるときはTrue
        
        for j in range(26):
            if( input[j] < Words[i][j] ):
                canCreate = False
                break
            else:
                canCreate = True
        
        if(canCreate == True):
            anagramSets.append(Words[i][26])
            return Words[i][:]
                
    # return anagramSets

countedDictionary = createCountedDictionary(data)    # 辞書の単語のアルファベットをカウントする

# 入力データの読み込み
f = open('large.txt','r')
inputData = f.read().splitlines()
f.close


outputfile = open('result.txt','w')

# 与えられたテキストからアナグラムを全て表示する
for input in range(len(inputData)):

    # 入力された単語から、文字以外を取り除く
    pattern = r'([a-zA-Z]*)'
    seikika = re.findall(pattern,inputData[input])  # 入力から全ての文字列を見つける
    seikika = "".join(sorted(seikika))  # 見つけた文字列を結合する
    seikika = str.lower(seikika)        # 全ての文字列を小文字にする

    if(seikika == ""):
        sys.exit("文字列が与えられていません。プログラムを終了します。")

    # 入力された文字列に使用されているアルファベットを数えていく
    inputAlphabetCount = [0]*26
    for j in range(len(seikika)):
        inputAlphabetCount[(ord(seikika[j])-ord('a'))] += 1    # a:0 ~ z:25　の場所をインクリメント

    Answers = anagramSearch(inputAlphabetCount,countedDictionary)   # 答えを格納する

    outputfile.write(Answers[26]+'\n')  # 最もよいスコアをファイルへ記入


outputfile.close()

'''
MY SCORE
small.txt 193
medium.txt 18911
large.txt 244642
large.txtのbestアナグラムを出力するときに、25秒で513個ほどの計算量。8分くらい待つ。遅すぎる、、、？
→辞書内にスコアを格納して、点数で辞書をソートする形式へ変更すると10秒ほどの実行時間になった(5/28)
'''

'''
聞きたいこと(5/28)

スコア計算をどこでやるのが最もいいのか？
<calculateBestScore内>
全ての解答が入った配列を引数として計算している
×再度どのアルファベットが使用されているか一字ずつ見てしまっている
〇答えではないとわかっている単語のスコアを計算しなくともよい

N回の計算量？

<anagramSearch内>
〇単語のアルファベットの数を予め計算していて、その数をもとに判定している
×アナグラムを作成できない単語のスコアも途中までではあるけれど計算してしまうことになる

（存在するアナグラムの数）× （その文字数）の計算量？

→今回最適なのは、辞書内に配置すること！！実行時間もとても早くなった！！
'''