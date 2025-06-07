

# https://docs.google.com/document/d/1H6mhc7Dje0BTeIDAmCIy4GBOUC3Y1uKG8iq4qOq5QYs/edit?tab=t.0



def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiplication(line, index):
    token = {'type': 'MULT'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def read_leftBracket(line, index):
    token = {'type': 'LEFT_BRACKET'}
    return token, index + 1

def read_rightBracket(line, index):
    token = {'type': 'RIGHT_BRACKET'}
    return token, index + 1

def read_abs(line, index):
    # token = {'type':'ABS'}
    token = {'type':'FUNC','name':'ABS'}
    return token, index + 3

def read_int(line, index):
    token = {'type':'FUNC','name':'INT'}
    return token, index + 3

def read_round(line, index):
    token = {'type':'FUNC','name':'ROUND'}
    return token, index + 5

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            if line[index-1]== '-' and(line[index-2] == '*' or line[index-2]== '/'):    #2*-4にも対応
                tokens.pop()    # マイナスを取り除く
                (token, index) = read_number(line, index)
                token['number'] = - token['number'] # 値をマイナスにする
            else:
                (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_leftBracket(line, index)
        elif line[index] == ')':
            (token, index) = read_rightBracket(line, index)
        elif line[index:index+3] == 'abs':
            (token, index) = read_abs(line, index)
        elif line[index:index+3] == 'int':
            (token, index) = read_int(line, index)
        elif line[index:index+5] == 'round':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    # print(tokens)
    return tokens

# 掛け算と割り算
def evaluate_multiplication_divide(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            
            if tokens[index - 1]['type'] == 'MULT':
                mult = tokens[index-2]['number'] * tokens[index]['number']
                tokens[index-2:index+1] = [{'type': 'NUMBER', 'number': mult}]
                index -= 2
            elif tokens[index - 1]['type'] == 'DIV':
                if tokens[index] == 0:
                    raise ZeroDivisionError("division by zero")
                div = tokens[index-2]['number'] / tokens[index]['number']
                tokens[index-2:index+1] = [{'type': 'NUMBER', 'number': div}]
                index -=2
        index += 1
        
    return tokens

# 足し算と引き算
def evaluate_plus_minus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

# 四則演算
def evaluate_four_operation(tokens):
    evaluate_multiplication_divide(tokens)
    return evaluate_plus_minus(tokens)

# 左括弧のindexを渡すと、その括弧の対の右括弧までを計算する
def evaluate_inside_bracket(tokens, LeftBracketIndex):
    index = LeftBracketIndex + 1    # 左括弧の次の文字から探索
    RightBracketIndex = 0   # 右括弧の位置を保存
    bracket_tokens = [] # 括弧内の数式を保存
    # 右括弧が見つかるまで、bracket_tokensに入れる
    while tokens[index]['type'] != 'RIGHT_BRACKET':
        if tokens[index]['type'] == 'LEFT_BRACKET': # 再帰的に処理
            evaluate_inside_bracket(tokens, index)
        elif tokens[index]['type'] == 'ABS':    # abs関数が見つかったとき
            evaluate_abs_func(tokens, index)
        bracket_tokens.append(tokens[index])
        index += 1
    tokens[LeftBracketIndex : index + 1] = [{'type': 'NUMBER', 'number': evaluate_four_operation(bracket_tokens)}]  # 左括弧～右括弧までを、その中を計算したトークンで置き換える
    return tokens

# 関数のindexを渡すと、その括弧の対の右括弧までを計算する
def evaluate_func(tokens, funcIndex):
    index = funcIndex + 1   # 関数の左括弧
    func_tokens = []

    while tokens[index-1]['type'] != 'RIGHT_BRACKET':   # 右括弧が見つかるまで繰り返す
        if tokens[index]['type'] == 'FUNC': # 再度関数が来た時は再帰
            evaluate_func(tokens,index)
        elif tokens[index-1]['type'] != 'FUNC' and tokens[index]['type'] == 'LEFT_BRACKET': # 関数内に、関数以外の括弧を含む式があったとき
            evaluate_inside_bracket(tokens,index)
        func_tokens.append(tokens[index])
        index += 1
    
    # ここまで来た時、func()の括弧の中には関数は入っていないはず
    # print(func_tokens)
    x = evaluate_inside_bracket(func_tokens,0)
    x = x[0]['number']
    
    if tokens[funcIndex]['name'] == 'ABS':
        tokens[funcIndex : index] = [{'type': 'NUMBER', 'number': abs(x)}]
    elif tokens[funcIndex]['name'] == 'INT':
        tokens[funcIndex : index] = [{'type': 'NUMBER', 'number': int(x)}]
    elif tokens[funcIndex]['name'] == 'ROUND':
        tokens[funcIndex : index] = [{'type': 'NUMBER', 'number': round(x)}]
    
    return tokens


def evaluate(tokens):

    index = 0
    while index < len(tokens):
        # 関数がでてきたら、その括弧内を全て計算する
        if tokens[index]['type'] == 'FUNC':
            tokens = evaluate_func(tokens,index)
        index += 1

    # evaluate_func(tokens,0)
    index = 0
    # ()内→積商→和差の順に計算
    while index < len(tokens):
        # 左括弧がでてきたら、その括弧内を全て計算する
        if tokens[index]['type'] == 'LEFT_BRACKET':
            tokens = evaluate_inside_bracket(tokens,index)
        index += 1

    return evaluate_four_operation(tokens)


def test(line):
    try:
        tokens = tokenize(line)
        actual_answer = evaluate(tokens)
        expected_answer = eval(line)
        if abs(actual_answer - expected_answer) < 1e-8:
            print("PASS! (%s = %f)" % (line, expected_answer))
        else:
            print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))
    except ZeroDivisionError as e:
        print("ERROR!" , e)

# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("abs(int(-2.34)*(-1))+round(2.34*abs(int(-45/4)))")    # 全部入れ子構造のとき
    test("abs(2-3)+round(234.342)/int(-342)")  
    test("(abs(-2.3-abs(-3))+1)*(abs(-2*(-4))+2)")   # 絶対値関数の追加
    test("(2+3)*(4-6)") # 括弧の実装
    test("((3+4)*(6+1))*((5.2-3.4)*(24/(2*3)))")    # 括弧が複数回存在するとき
    test("4-2*3+1+1/2") # 掛け算割り算(kadai1)
    test("-3*-2*4*1") # 何回もかけたり割ったりする(kadai1)
    test("2/0")   # 0で割る(kadai1)
    test("1/2+2*4*3")
    test("1+2")
    test("1.0+2.1-3")
    print("==== Test finished! ====\n")

run_test()

# while True:
#     print('> ', end="")
#     line = input()
#     tokens = tokenize(line)
#     answer = evaluate(tokens)
#     print("answer = %f\n" % answer)

while True:
    print('> ', end="")
    line = input()
    try:
        tokens = tokenize(line)
        answer = evaluate(tokens)
        print("answer = %f\n" % answer)
    except ZeroDivisionError as e:
        print(e)