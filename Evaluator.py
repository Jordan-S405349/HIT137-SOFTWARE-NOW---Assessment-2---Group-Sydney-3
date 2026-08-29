"""Question 2 Part 1 - Jordan Then Ryan S405349"""


"""   Tokenisation   """

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
    
    # This while loop will go through the string into one character
    while index < length:
        character =  expression[index]
        
        # Will skip the whitespace (not include in character token)
        if character.isspace():
            index += 1
            continue
        
        # it will collect every digit in numbers
        if character.isdigit():
            start = index # start point
            index += 1
            
            # it will keep counting the digits while it last
            # it also can handle multi digit numbers
            while index < length and expression[index].isdigit():
                index += 1
            
            # To able to count decimal point
            if index < length and expression[index] == ".":
                
                # The "." must followed by at least one digit
                # No digit raise error (and invalid number("6."))
                if index + 1 < length and expression[index + 1].isdigit():
                    index += 1 # it will skip over the "."
                    
                    while index < length and expression[index].isdigit():
                        index += 1
                
                else:
                    raise ValueError("" + str(start))
            
            # The expression[start:index] save the collection of numbers
            token.append(('NUM', expression[start:index]))
            continue
        
        # Binary operator: "+-*/%^"
        # it will check and count the operator string
        if character in binary_operator:
            token.append(("OP", character))
            index += 1
            continue
        
        # Cheking the left parentheses
        if character == "(":
            token.append(("LPAREN", "("))
            index += 1
            continue
        
        # Cheking the right parentheses
        if character == ")":
            token.append(("RPAREN", ")"))
            index += 1
            continue
        
        # Raise the value error if the character is not matched
        raise ValueError("" + character + "" + str(index))
    
    # Every token will ends with "END" token
    token.append(("END", ""))
    return token


def token_into_string(token):
    """Formatting the token as [OP:-] [NUM:5] [END]
    """
    
    part = []
    
    for type, value in token:
        # it make sure it only shown as "[END]"
        if type == "END":
            part.append("[END]")
        else:
            part.append("[" + type + ":" + value + "]")
    return " ".join(part)

"""Creating recursive descent parser function"""

def recursive_parse(token):
    """parse all the token stream into a tree
    and raises the ValueError on failure
    """
    
    pos = [0]
    tree = parse_expression(token, pos) 
    expecting(token, pos, "END")
    return tree


def peeking(token, pos):
    """It will peeking the tokens without manipulation"""
    return token[pos[0]]


def advancing(token, pos):
    """Returning the current token and move the cursor forward by one"""
    advance = token[pos[0]]
    pos[0] += 1
    return advance


def expecting(token, pos, type):
    """It will take the current token only if it matches with the expexted type.
    It will raised an error if its not match.
    It will ensure the '(' followed by ')'
    """
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
        
        if term[0] == "OP" and term[1] in ("*", "/", "%"):
            operator = advancing(token, pos)[1]
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
    """This is level 3: unary '-' and recursive so '--5' ---> (neg (negative 5)) """
    unary = peeking(token, pos)
    
    if unary[0] == "OP" and unary[1] == "-":
        advancing(token, pos)
        operand = parse_unary(token, pos)
        return ("neg", operand)
    
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
    """This is the innermost level.
    A single number and parenthesised sub expression.
    When it see the '(', it will call the parse_expression again.
    It will handling the parenthesised sub-expression,
    because the parentheses can appear inside the parentheses."""
    primary = peeking(token, pos)
    
    if primary[0] == "NUM":
        advancing(token, pos)
        return ("num", primary[1])
    
    if primary[0] == "LPAREN":
        advancing(token, pos)                   # taking the "("
        node = parse_expression(token, pos)     # recurse back to the top level
        expecting(token, pos, "RPAREN")         # ensure it followed by ")"
        
        # It will implicit the multiplication after the closing parenthesis
        # Ex: "(6)7" or "(6)(7)" will be "(6)*7" or "(6)*(7)"
        if peeking(token, pos)[0] in ("NUM", "LPAREJ"):
            right = parse_unary(token, pos)
            return ("Binop", "*", node, right)
        return node
    
    # Raise the ValueError if the token cant start a valid factor
    raise ValueError("Unexpected token found!" + str(primary))


"""Building tree contruction"""

def tree_into_string(tree):
    t = tree[0]
    
    if t == "num":
        return format_number_literal(tree[1])
    
    if t == "neg":
        # negative unary will prints as "(neg [operation])"
        return "(neg " + tree_into_string(tree[1]) + ")"
    
    if t == "Binop":
        # ensuring binary operation prints as "([OP] [Left] [Right])"
        operator, left, right = tree[1], tree[2], tree[3]
        return "(" + operator + " " + tree_into_string(left) + " " + tree_into_string(right) + ")"
    
    # Adding the raise just for incase with bad tree shape
    raise ValueError("Unrecognise tree node: " + str(tree))


def format_number_literal(raw):
    """Ensuring the float number does not printed with '.'.
    '67' stays as '67'.
    if a decimal number stays as a decimal number"""
    if "." in raw:
        value = float(raw)
        
        if value == int(value):
            return str(int(value))
    
    return raw
