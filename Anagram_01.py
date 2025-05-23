# 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る
# 自分でテストケースを作って、確認してね♪

# 辞書ファイルの取得、1行ごとに保存
f = open('words.txt','r')
data = f.read().splitlines()    # 1行ごとにデータを取得。辞書データの\nは除去。
f.close()

# 新しい辞書を作成する関数
def createSortedDictionary( words ):

    sortedDictionary = []

    for i in words:
        sortedWord = ''.join(sorted(i))    # iをソートしたものを結合する
        sortedDictionary.append( sortedWord , i )    # (ソート済み単語、元の単語)をアペンド

    sortedDictionary = sorted(sortedDictionary) # 単語内をソートした辞書をさらにソート

    return sortedDictionary


createSortedDictionary(data)

    