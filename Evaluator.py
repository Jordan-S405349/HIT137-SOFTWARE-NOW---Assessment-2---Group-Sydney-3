"""Question 2 Part 1 - Jordan Then Ryan S405349"""
# Tokenisation

# declaring binary operator variable
binary_operator = "+-*/%^"


def tokenisation(expression):
    """This def function is converting the raw expression int list of (type,  value) tuples
    that have edning with an ("END", "") token and it raises ValueError on any character
    that are not numbers, binary operator, and parenthesis
    """
    # Declaring the varibles (token(list), index(int), length(len of expression))
    token = []
    index = 0
    length = len(expression)
    
    while index < length:
        character =  expression[index]
        
        if character.isspace():
            index += 1
            continue
        
        if character.isdigit():
            start = index
            index += 1
            
            while index < length and expression[index].isdigit():
                index += 1
            
            if index < length and expression[index] == ".":
                
                if index + 1 < length and expression[index + 1].isdigit():
                    index += 1
                    
                    while index < length and expression[index].isdigit():
                        index += 1
                
                else:
                    raise ValueError("" + str(start))
            
            token.append(('NUM', expression[start:index]))
            continue
        
        if character in binary_operator:
            token.append(("OP", character))
            index += 1
            continue
        
        if character == "(":
            token.append(("LPAREN", "("))
            index += 1
            continue
        
        if character == ")":
            token.append(("RPAREN", ")"))
            index += 1
            continue
        
        raise ValueError("" + character + "" + str(index))
    
    token.append(("END", ""))
    return token


def token_into_string(token):
    """Formatting the token as [OP:-] [NUM:5] [END]
    """
    
    part = []
    
    for type, value in token:
        if type == "END":
            part.append("[END]")
        else:
            part.append("[" + type + ":" + value + "]")
    
    return " ".join(part)

"""Creating recursive descent parser function"""

def recursive_parse(token):
    """parse all the token stream into a tree
    and raises the ValueErro on failure
    """
    
    pos = [0]
    tree = parse_expression(token, pos) 
    expecting(token, pos, "END")
    return tree


def peeking(token, pos):
    return token[pos[0]]


def advancing(token, pos):
    advance = token[pos[0]]
    pos[0] += 1
    return advance


def expecting(token, pos, type):
    expect = peeking(token, pos)
    
    if expect[0] != type:
        raise ValueError(f"Expecting {type} but got {str(expect)}")
    return advancing(token, pos)


def parse_expression(token, pos):
    """This is level 1: Operator + and - with left associativity"""
    node = parse_term(token, pos)
    
    while peeking(token, pos)[0] == "OP" and peeking(token, pos)[1] in ("+", "-"):
        operator = advancing(token, pos)[1]
        right = parse_term(token, pos)
        node = ("Binop", operator, node, right)
    return node


def parse_term(token, pos):
    """This is level 2: *, /, % and implicit multiplication
    with left associativity
    """
    node = parse_unary(token, pos)
    
    while True:
        term = peeking(token, pos)
        
        if term[0] == "OP" and term[1] in ("*", "/", "5"):
            operator = advancing(token, pos)
            right = parse_unary(token, pos)
            node = ("Binop", operator, node, right)
        
        elif term[0] == "LPAREN":
            right = parse_unary(token,pos)
            node = ("Binop", "*", node, right)
        
        elif term[0] == "NUM":
            raise ValueError("Numbers without operator are invalid")
        
        else:
            break
        
    return node


def parse_unary(token, pos):
    """This is level 3: unary '-' and recursive so '--5' ---> (negative (negative 5)) """
    unary = peeking(token, pos)
    
    if unary[0] == "OP" and unary[1] == "-":
        advancing(token, pos)
        operand = parse_unary(token, pos)
        return ("negative", operand)
    
    if unary[0] == "OP" and unary[1] == "+":
        raise ValueError("Unary '+' is not supported!!!")
    
    return power_parse(token, pos)


def power_parse(token, pos):
    """This is level 4: '^' with right associativity"""
    base = primary_parse(token, pos)
    
    if peeking(token, pos)[0] == "OP" and peeking(token, pos)[1] == "^":
        advancing(token, pos)
        exponent = parse_unary(token, pos)
        return ("Binop", "^", base, exponent)
    
    return base


def primary_parse(token, pos):
    """"""
    primary = peeking(token, pos)
    
    if primary[0] == "NUM":
        advancing(token, pos)
        return ("num", primary[1])
    
    if primary[0] == "LPAREN":
        advancing(token, pos)
        node = parse_expression(token, pos)
        expecting(token, pos, "RPAREN")
        
        if peeking(token, pos)[0] in ("NUM", "LPAREJ"):
            right = parse_unary(token, pos)
            return ("Binop", "*", node, right)
        return node
    
    raise ValueError("Unexpected token found!" + str(primary))


"""Building tree contruction"""

def tree_into_string(tree):
    t = tree[0]
    
    if t == "num":
        return format_number_literal(tree[1])
    
    if t == "negative":
        return "(negative" + tree_into_string(tree[1]) + ")"
    
    if t == "Binop":
        operator, left, right = tree[1], tree[2], tree[3]
        return "(" + operator + " " + tree_into_string(left) + " " + tree_into_string(right) + ")"
    
    raise ValueError("Unrecognise tree node: " + str(tree))


def format_number_literal(raw):
    """ """
    if "." in raw:
        value = float(raw)
        
        if value == int(value):
            return str(int(value))
    
    return raw
print()