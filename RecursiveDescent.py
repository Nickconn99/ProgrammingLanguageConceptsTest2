"""
NICK CONN
#Test 2
Recursive descent algorithm

Requires file 'rdInput.txt' to run
Program takes one expression in 'rdInput.txt' as input.

The program returns input expression, a list of each lexeme along with its associated token, and whether or not the expression follows the correct syntax.


Sample expressions that are in correct syntax:

if (x < 10) { if (y > 5) { z = 1; }; };
if (x==0){x=y;}; while(x>0){x=x-1;}; int x;
if (a == 3) { b = c * 2; }; else { b = 5; };
if (x==0){x=y;}else{x=2.4;}; while(x>0){x=x-1;}; int z;
"""
import re


current_token_index = 0

def parse(tokens):
    global current_token_index
    current_token_index = 0
    if stmt_list(tokens):
        return True
    return False

def stmt_list(tokens):
    global current_token_index
    if stmt(tokens):
        if tokens[current_token_index] == 'SEMICOLON':
            current_token_index += 1
            if stmt_list(tokens):
                return True
            return False
        return False
    return True

def stmt(tokens):
    if if_stmt(tokens) or block(tokens) or assign(tokens) or declare(tokens) or while_loop(tokens):
        return True
    return False

def while_loop(tokens):
    global current_token_index
    if tokens[current_token_index] == 'while':
        current_token_index += 1
        if tokens[current_token_index] == 'LEFT_PAREN':
            current_token_index += 1
            if bool_expr(tokens):
                if tokens[current_token_index] == 'RIGHT_PAREN':
                    current_token_index += 1
                    if block(tokens):
                        return True
                return False
            return False
        return False
    return False

def if_stmt(tokens):
    global current_token_index
    if tokens[current_token_index] == 'if':
        current_token_index += 1
        if tokens[current_token_index] == 'LEFT_PAREN':
            current_token_index += 1
            if bool_expr(tokens):
                if tokens[current_token_index] == 'RIGHT_PAREN':
                    current_token_index += 1
                    if block(tokens):
                        if tokens[current_token_index] == 'else':
                            current_token_index += 1
                            if block(tokens):
                                return True
                            return False
                        return True
                return False
            return False
        return False
    return False

def block(tokens):
    global current_token_index
    if tokens[current_token_index] == 'LEFT_BRACE':
        current_token_index += 1
        if stmt_list(tokens):
            if tokens[current_token_index] == 'RIGHT_BRACE':
                current_token_index += 1
                return True
            return False
        return False
    return False

def declare(tokens):
    global current_token_index
    if tokens[current_token_index] == 'DataType':
        current_token_index += 1
        if tokens[current_token_index] == 'ID':
            current_token_index += 1
            while tokens[current_token_index] == 'COMMA':
                current_token_index += 1
                if tokens[current_token_index] == 'ID':
                    current_token_index += 1
                else:
                    return False
            return True
        return False
    return False

def assign(tokens):
    global current_token_index
    if tokens[current_token_index] == 'ID':
        current_token_index += 1
        if tokens[current_token_index] == 'ASSIGN':
            current_token_index += 1
            if expr(tokens):
                return True
            return False
        return False
    return False

def expr(tokens):
    global current_token_index
    if term(tokens):
        while tokens[current_token_index] == 'OP':
            current_token_index += 1
            if term(tokens):
                continue
            else:
                return False
        return True
    return False

def term(tokens):
    global current_token_index
    if fact(tokens):
        while tokens[current_token_index] in ['*', '/', '%']:
            current_token_index += 1
            if fact(tokens):
                continue
            else:
                return False
        return True
    return False

def fact(tokens):
    global current_token_index
    if tokens[current_token_index] == 'ID' or tokens[current_token_index] == 'INT_LIT' or tokens[current_token_index] == 'FLOAT_LIT':
        current_token_index += 1
        return True
    elif tokens[current_token_index] == 'LEFT_PAREN':
        current_token_index += 1
        if expr(tokens):
            if tokens[current_token_index] == 'RIGHT_PAREN':
                current_token_index += 1
                return True
        return False
    else:
        return False
    
def bool_expr(tokens):
    global current_token_index
    if bool_term(tokens):
        while tokens[current_token_index] in ['AND', 'OR']:
            current_token_index += 1
            if bool_term(tokens):
                continue
            else:
                return False
        return True
    return False

def bool_term(tokens):
    global current_token_index
    if bool_fact(tokens):
        while tokens[current_token_index] in ['<', '>', '==', '!=', '<=', '>=']:
            current_token_index += 1
            if bool_fact(tokens):
                continue
            else:
                return False
        return True
    return False

def bool_fact(tokens):
    global current_token_index
    if tokens[current_token_index] == 'TRUE' or tokens[current_token_index] == 'FALSE':
        current_token_index += 1
        return True
    elif tokens[current_token_index] == 'ID':
        current_token_index += 1
        if tokens[current_token_index] == 'EQ':
            current_token_index += 1
            if expr(tokens):
                return True
        return False
    elif tokens[current_token_index] == 'NOT':
        current_token_index += 1
        if bool_fact(tokens):
            return True
        return False
    elif tokens[current_token_index] == 'LEFT_PAREN':
        current_token_index += 1
        if bool_expr(tokens):
            if tokens[current_token_index] == 'RIGHT_PAREN':
                current_token_index += 1
                return True
        return False
    else:
        return False
    
def tokenize(input_string):
    # Split input string into separate words
    words = re.findall('\w+|\S', input_string)

    # Define a list of keywords
    keywords = ['if', 'else', 'while', 'DataType']


    # Create a list to hold the tokens
    tokens = []
    tokenValues = []

    # Iterate over the words and classify them as tokens
    i = 0
    while i < len(words):
        word = words[i]
        if word in keywords:
            tokens.append(word)
            tokenValues.append((word.upper(), word))
        elif word == 'int' or word == 'float' or word == 'bool':
            tokens.append('DataType')
            tokenValues.append(('DataType', word))
        elif word == '(':
            tokens.append('LEFT_PAREN')
            tokenValues.append(('LEFT_PAREN', '('))
        elif word == ')':
            tokens.append('RIGHT_PAREN')
            tokenValues.append(('RIGHT_PAREN', ')'))
        elif word == '{':
            tokens.append('LEFT_BRACE')
            tokenValues.append(('LEFT_BRACE', '{'))
        elif word == '}':
            tokens.append('RIGHT_BRACE')
            tokenValues.append(('RIGHT_BRACE', '}'))
        elif word == ';':
            tokens.append('SEMICOLON')
            tokenValues.append(('SEMICOLON', ';'))
        elif word == ',':
            tokens.append('COMMA')
            tokenValues.append(('COMMA', ','))
        elif word == '=':
            if words[i+1] == '=':
                tokens.append('BOOL_OP')
                tokenValues.append(('BOOL_OP', '=='))
                i += 1
            else:
                tokens.append('ASSIGN')
                tokenValues.append(('ASSIGN', '='))
        elif word == '&':
            if words[i+1] == '&':
                tokens.append('AND')
                tokenValues.append(('AND', '&&'))
                i += 1
        elif word == '|':
            if words[i+1] == '|':
                tokens.append('OR')
                tokenValues.append(('OR', '||'))
                i += 1       
        elif word == '<':
            if words[i+1] == '=':
                tokens.append('BOOL_OP')
                tokenValues.append(('BOOL_OP', '<='))
                i += 1
            else:
                tokens.append('BOOL_OP')
                tokenValues.append(('BOOL_OP', '<'))
        elif word == '>':
            if words[i+1] == '=':
                tokens.append('BOOL_OP')
                tokenValues.append(('BOOL_OP', '>='))
                i += 1
            else:
                tokens.append('BOOL_OP')
                tokenValues.append(('BOOL_OP', '>'))
        elif word == '!':
            if words[i+1] == '=':
                tokens.append('BOOL_OP')
                tokenValues.append(('BOOL_OP', '!='))
                i += 1
        elif word == '+' or word == '-' or word == '/' or word == '*' or word == '%':
            tokens.append('OP')
            tokenValues.append(('OP', word))
        elif word.isnumeric():
            tokens.append('INT_LIT')
            tokenValues.append(('INT_LIT', word))
        elif '.' in word and all(char.isdigit() or char == '.' for char in word):
            tokens.append('FLOAT_LIT')
            tokenValues.append(('FLOAT_LIT', word))
        elif word.isidentifier():
            tokens.append('ID')
            tokenValues.append(('ID', word))
        elif word.isspace():
            pass
        else:
            raise ValueError(f"Unrecognized token: {word}")
        i += 1

    return tokens, tokenValues





with open("rdInput.txt") as f:
    data = f.read().replace('\n', '')

    tokens, tokenValues = tokenize(data)
    print(data + "\n")
    print("Tokens:\n")
    print(tokenValues)
    print("\n")
    if(parse(tokens) == True):
        print("The input is correct syntax!")
    else:
        print("The input is incorrect syntax!")


