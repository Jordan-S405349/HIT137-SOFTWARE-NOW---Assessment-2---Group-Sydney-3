from Evaluator import tokenisation, token_into_string

"""checking the tokenisation to ensure they work properly
"""
def check_tokenisation(expression, expected_token_result):
    try:
        result =  token_into_string(tokenisation(expression))
    except ValueError:
        result = "Something is wrong!"
    
    status = "Good to go!" if result == expected_token_result else "Check again!"
    print(f"[{status}] tokenisation({expression!r})")
    
    if status == "Check again!":
        print(f"{"Expected":35}: {expected_token_result}")
        print(f"{"What it gives":35}: {result}")
    return status == "Good to go!"

example = [
    ("3 + 5", "[NUM:3] [OP:+] [NUM:5] [END]"),
    ("2 + 3*4", "[NUM:2] [OP:+] [NUM:3] [OP:*] [NUM:4] [END]"),
    ("-(3 + 4)", "[OP:-] [LPAREN:(] [NUM:3] [OP:+] [NUM:4] [RPAREN:)] [END]"),
    ("--5", "[OP:-] [OP:-] [NUM:5] [END]"),
    ("3*(10 - 2)", "[NUM:3] [OP:*] [LPAREN:(] [NUM:10] [OP:-] [NUM:2] [RPAREN:)] [END]"),
    ("3 @ 5", "Something is wrong!"),
    ("1 / 0", "[NUM:1] [OP:/] [NUM:0] [END]")
]

good = sum(check_tokenisation(expression, expected_token_result) for expression, expected_token_result in example)
print(f"\n{good}/{len(example)} is correct.") # The result: 7/7 all is correct.