# 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
# 自分でテストケースを作って、確認してね♪


# テストケース
test = 'ta'   

# 辞書ファイルの取得、1行ごとに保存
f = open('words.txt','r')
data = f.read().splitlines()    # 1行ごとにデータを取得。辞書データの\nは除去。
f.close()

# 新しい辞書(全ての単語をソートしてから、辞書全体もソートする)を作成する関数
def createSortedDictionary( words ):

    sortedDictionary = []

    for i in words:
        sortedWord = ''.join(sorted(i))    # iをソートしたものを結合する
        sortedDictionary.append( [sortedWord , i ])    # (ソート済み単語、元の単語)をアペンド

    sortedDictionary = sorted(sortedDictionary) # 単語内をソートした辞書をさらにソート

    return sortedDictionary


sortedDictionary = createSortedDictionary(data)    # 辞書をソートする

sortedInput = ''.join(sorted(test))    # テストケースをソートする


# ソートした単語(test) が、辞書(Words)の中にあるかを二分探索で調べていく
def binarySearch( test , Words):
    
    high = len(data)-1
    low = 0
    
    while(low <= high):
        middle = int (( high + low ) / 2)

        if( test == Words[middle][0] ): # 真ん中が
            return Words[middle][:]
        elif( test < Words[middle][0]):
            high = middle - 1
        else:
            low = middle + 1




# print(middle)


print(binarySearch(sortedInput,sortedDictionary))