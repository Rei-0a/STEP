# 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
# 自分でテストケースを作って、確認してね♪

import re
import sys

# テストケース
# test = 'asdgawega'  # 存在しないとき
# test = 'a ".t22'    # 文字以外が沢山ある
# test = 'cat'    # 複数のアナグラムを持つとき
# test = '  '
# test = 'cAtcHlands' # 長くて大文字も含まれているとき
test = 'a'

# 辞書ファイルの取得、1行ごとに保存
f = open('words.txt','r')
data = f.read().splitlines()    # 1行ごとにデータを取得。辞書データの\nは除去。
f.close()

# 新しい辞書(全ての単語をソートしてから、辞書全体もソートする)を作成する関数
def createSortedDictionary( words ):

    sortedDictionary = []

    # sortedf = open('sortedWords.txt','w')

    for i in words:
        sortedWord = ''.join(sorted(i))    # iをソートしたものを結合する
        sortedDictionary.append( [sortedWord , i ])    # (ソート済み単語、元の単語)をアペンド
        # sortedf.write(sortedWord+"\n")

    sortedDictionary = sorted(sortedDictionary) # 単語内をソートした辞書をさらにソート

    # sortedf.close()
    return sortedDictionary

sortedDictionary = createSortedDictionary(data)    # 辞書をソートする

# 入力された単語から、文字以外を取り除く
pattern = r'([a-zA-Z]*)'
seikika = re.findall(pattern,test)  # 入力から全ての文字列を見つける
seikika = "".join(sorted(seikika))  # 見つけた文字列を結合する
seikika = str.lower(seikika)        # 全ての文字列を小文字にする
sortedInput = ''.join(sorted(seikika))    # テストケースをソートする

if(sortedInput == ""):
    sys.exit("文字列が与えられていません。プログラムを終了します。")
# sortedInput = sortedInput.replace(" ","")
# sortedInput = sortedInput.replace("\"","")
# sortedInput = sortedInput.replace(".","")

# ソートした単語(test) が、辞書(Words)の中にあるかを二分探索で調べていく
def binarySearch( test , Words):
    
    high = len(data)-1
    low = 0

    hasfound = 0 # 単語が見つかったときは1、見つからなかったときは0にする
    
    while(low <= high):
        middle = int (( high + low ) / 2)
        if( test == Words[middle][0] ):
            hasfound = 1
            break
        elif( test < Words[middle][0]):
            high = middle - 1
        else:
            low = middle + 1
    
    if(hasfound == 0):
        # whileを抜けてしまったとき、そのanagramは存在しない
        return 0
    
    AnagramSets = []    
    AnagramSets.append(Words[middle][:])

    # 前後に同じAnagramがないか探す
    before = 1
    after = 1
    count = 0
    while((before == 1 or after == 1)and (middle + count > 0) and (middle - count > 0)):
        count += 1

        if(before == 1):
            if( Words[middle+count][0] == test):
                # print("before true",Words[middle+count][:])
                AnagramSets.append(Words[middle+count][:])
            else:
                # print("before false",Words[middle+count][:])
                before = 0
        if(after == 1):
            if( Words[middle-count][1] == test):
                # print("after true",Words[middle-count][:])
                AnagramSets.append(Words[middle-count][:])
            else:
                # print("after false",Words[middle-count][:])
                after = 0

    return AnagramSets
    



Answers = binarySearch(sortedInput,sortedDictionary)

if(Answers == 0 ):
    print(test,"'s Anagram doesn't exist")
else:
    print(test,"'s anagram is")
    for answer in Answers:
        print(answer[1])
