

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


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

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

def evaluate(tokens):
    evaluate_multiplication_divide(tokens)
    return evaluate_plus_minus(tokens)


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
    test("4-2*3+1+1/2") # 掛け算割り算
    test("3*2*4*1") # 何回もかけたり割ったりする
    test("2/0")   # 0で割る
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