import unittest
from Evaluator import tokenisation, token_into_string, recursive_parse, tree_into_string

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
print(f"\n{good}/{len(example)} is correct.") # The result: 7/7

class TestTokenisation(unittest.TestCase):
    def test_addition(self):
        token = ("3 + 5")
        self.assertEqual(
            token_into_string(tokenisation(token)),
            "[NUM:3] [OP:+] [NUM:5] [END]"
        )

    def test_binary_operator(self):
        token = tokenisation("2 + 3*4")
        self.assertEqual(
            token_into_string(token),
            "[NUM:2] [OP:+] [NUM:3] [OP:*] [NUM:4] [END]"
        )

    def test_parentheses(self):
        token = tokenisation("-(3 + 4)")
        self.assertEqual(
            token_into_string(token),
            "[OP:-] [LPAREN:(] [NUM:3] [OP:+] [NUM:4] [RPAREN:)] [END]"
        )

    def test_minus_not_into_number(self):
        token = tokenisation("-5")
        self.assertEqual(
            token_into_string(token),
            "[OP:-] [NUM:5] [END]"
        )

    def double_minus(self):
        token = tokenisation("--5")
        self.assertEqual(
            token_into_string(token),
            "[OP:-] [OP:-] [NUM:5] [END]"
        )

    def decimal_number(self):
        token = tokenisation("3.14 + 2.71")
        self.assertEqual(
            token_into_string(token),
            "[NUM:3.14] [OP:+] [NUM:2.71] [END]"
        )

    def test_whitespace(self):
        token = tokenisation("  3 +   5 ")
        self.assertEqual(
            token_into_string(token),
            "[NUM:3] [OP:+] [NUM:5] [END]"
        )

    def test_empty_expression(self):
        token = tokenisation("")
        self.assertEqual(
            token_into_string(token),
            "[END]"
        )

    def test_invalid_character(self):
        with self.assertRaises(ValueError):
            tokenisation("3 @ 5")

    def test_uncomplete_decimal(self):
        with self.assertRaises(ValueError):
            tokenisation("3. + 5")


class ParseExpressionTest(unittest.TestCase):

    def test_addition_tree(self):
        tree = recursive_parse(tokenisation("3 + 5"))
        self.assertEqual(
            tree_into_string(tree), 
            "(+ 3 5)"
        )
    
    def testing_multiplication_without_whitespace(self):
        tree = recursive_parse(tokenisation("3 + 3*4"))
        self.assertEqual(
            tree_into_string(tree),
            "(+ 3 (* 3 4))"
        )
    
    def parantheses_override_precendence_testing(self):
        tree = recursive_parse(tokenisation("(2 + 3) * 5"))
        self.assertEqual(
            tree_into_string(tree),
            "(* (+ 2 3) 5)"
            )
    
    def left_associativity_subtraction_testing(self):
        tree = recursive_parse(tokenisation("6 - 7 - 1"))
        self.assertEqual(
            tree_into_string(tree),
            ("(- (- 6 7) 1)")
        )
    
    def right_associativity_power_testing(self):
        tree = recursive_parse(tokenisation("6^7^9"))
        self.assertEqual(
            tree_into_string(tree),
            "(^ 6 (^ 7 9))"
        )
    
    def power_bind_tighter_than_minus_testing(self):
        tree = recursive_parse(tokenisation("(-(6^6)"))
        self.assertEqual(
            tree_into_string(tree),
            "(negative (^ 6 6))"
        )
    
    def double_minus_tree_testing(self):
        tree = recursive_parse(tokenisation("--6"))
        self.assertEqual(
            tree_into_string(tree),
            "(negative (negative 6))"
        )
    
    def binary_minus_after_operator_testing(self):
        tree = recursive_parse(tokenisation("6 * -7"))
        self.assertEqual(
            tree_into_string(tree),
            "(* 6 (negative 7))"
        )
        
    def multiplication_number_then_parenthesis_testing(self):
        tree = recursive_parse(tokenisation("6(7+9)"))    
        self.assertEqual(
            tree_into_string(tree),
            "(* 6 (+ 7 9))"
        )
    
    def multiplication_with_parenthesis_testing(self):
        tree = recursive_parse(tokenisation("(6)(7)"))
        self.assertEqual(
            tree_into_string(tree),
            "(* 6 7)"
        )
    
    def bare_numbers_without_operator_testing(self):
        with self.assertRaises(ValueError):
            recursive_parse(tokenisation("6 7"))
    
    def missing_number_testing(self):
        with self.assertRaises(ValueError):
            recursive_parse(tokenisation("+7"))
    
    def parenthesis_error_testing(self):
        with self.assertRaises(ValueError):
            recursive_parse(tokenisation("(6 + 7"))
            
if __name__ == "__main__":
    unittest.main()