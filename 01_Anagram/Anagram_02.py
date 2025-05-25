# 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
# 自分でテストケースを作って、確認してね♪

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

# 新しい辞書(それぞれの単語をアルファベットを数えたもの)を作成する関数
def createCountedDictionary( words ):

    countedDictionary = []

    # sortedf = open('sortedWords_02.txt','w')

    for word in words:
        alphabetsCount = [0]*26
        for j in range(len(word)):
            alphabetsCount[(ord(word[j])-ord('a'))] += 1    # a:0 ~ z:25　の場所をインクリメント
        
        alphabetsCount.append(word)
        countedDictionary.append(alphabetsCount)
        # sortedf.write(str(alphabetsCount)+"\n")

    # sortedf.close()
    return countedDictionary

# アルファベットをカウントした単語(input) が、辞書(Words)の中にあるかを調べていく関数
def anagramSearch( input , Words):
    anagramSets= []
    
    for i in range(len(Words)):
        canCreate = 1
        for j in range(26):
            if( input[j] < Words[i][j] and canCreate == 1):
                canCreate = 0
                break
            else:
                canCreate = 1
        
        if(canCreate == 1):
            anagramSets.append(Words[i][26])
                
    return anagramSets

# 答えを全て出力する関数
def printAllAnswers( Answers ):

    if(Answers == []):
        print("There are no anagrams that can be made from"+seikika+"'s characters.")
    else:
        print("The anagrams that can be made from"+seikika+"'s these characters are as follows:")
        print('length = ',len(Answers))
        for i in range(len(Answers)):
            if(i < len(Answers)-1):
                print(Answers[i],end=', ')
            else:
                print(Answers[i],end = '\n\n')


countedDictionary = createCountedDictionary(data)    # 辞書の単語のアルファベットをカウントする

f = open('small.txt','r')
inputData = f.read().splitlines()
f.close

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

    # printAllAnswers(Answers)

