from Evaluator import tokenisation, token_into_string, recursive_parse, tree_into_string

def read_operator(path):
    operator = []
    
    with open(path, "r", newline="") as file:
        for line in file:
            lines = line.strip()
            if lines != "":
                operator.append(lines)
    return operator

if __name__ == "__main__":
    operators = read_operator("sample_input.txt")
    
    for operator in operators:
        print("Operator: " + operator)
        try:
            token = tokenisation(operator)
            print("Tokens: " + token_into_string(token))
        except ValueError as e:
            print("Tokens: ERROR")
            continue
        
        try:
            tree =recursive_parse(token)    
            print("Tree: " + tree_into_string(tree))
        except ValueError as e:
            print("Tree: ERROR")

"""Result:
Operator: 3 + 5
Tokens: [NUM:3] [OP:+] [NUM:5] [END]
Tree: (+ 3 5)
Operator: 2 + 3 * 4
Tokens: [NUM:2] [OP:+] [NUM:3] [OP:*] [NUM:4] [END]
Tree: (+ 2 (* 3 4))
Operator: -(3 + 4)
Tokens: [OP:-] [LPAREN:(] [NUM:3] [OP:+] [NUM:4] [RPAREN:)] [END]
Tree: (neg (+ 3 4))s
Operator: --5
Tokens: [OP:-] [OP:-] [NUM:5] [END]
Tree: (neg (neg 5))
Operator: (10 - 2) * 3 + -4 / 2
Tokens: [LPAREN:(] [NUM:10] [OP:-] [NUM:2] [RPAREN:)] [OP:*] [NUM:3] [OP:+] [OP:-] [NUM:4] [OP:/] [NUM:2] [END]
Tree: (+ (* (- 10 2) 3) (/ (neg 4) 2))
Operator: 3 @ 5
Tokens: ERROR
Operator: 1 / 0
Tokens: [NUM:1] [OP:/] [NUM:0] [END]
Tree: (/ 1 0)
"""