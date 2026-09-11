import unittest
from Evaluator import tokenisation, token_into_string, recursive_parse, tree_into_string


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

    def test_double_minus(self):
        token = tokenisation("--5")
        self.assertEqual(
            token_into_string(token),
            "[OP:-] [OP:-] [NUM:5] [END]"
        )

    def test_decimal_number(self):
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
    
    def test_parantheses_override_precendence_testing(self):
        tree = recursive_parse(tokenisation("(2 + 3) * 5"))
        self.assertEqual(
            tree_into_string(tree),
            "(* (+ 2 3) 5)"
            )
    
    def test_left_associativity_subtraction_testing(self):
        tree = recursive_parse(tokenisation("6 - 7 - 1"))
        self.assertEqual(
            tree_into_string(tree),
            ("(- (- 6 7) 1)")
        )
    
    def test_right_associativity_power_testing(self):
        tree = recursive_parse(tokenisation("6^7^9"))
        self.assertEqual(
            tree_into_string(tree),
            "(^ 6 (^ 7 9))"
        )
    
    def test_power_bind_tighter_than_minus_testing(self):
        tree = recursive_parse(tokenisation("-(6^6)"))
        self.assertEqual(
            tree_into_string(tree),
            "(neg (^ 6 6))"
        )
    
    def test_double_minus_tree_testing(self):
        tree = recursive_parse(tokenisation("--6"))
        self.assertEqual(
            tree_into_string(tree),
            "(neg (neg 6))"
        )
    
    def test_binary_minus_after_operator_testing(self):
        tree = recursive_parse(tokenisation("6 * -7"))
        self.assertEqual(
            tree_into_string(tree),
            "(* 6 (neg 7))"
        )
        
    def test_multiplication_number_then_parenthesis_testing(self):
        tree = recursive_parse(tokenisation("6(7+9)"))    
        self.assertEqual(
            tree_into_string(tree),
            "(* 6 (+ 7 9))"
        )
    
    def test_multiplication_with_parenthesis_testing(self):
        tree = recursive_parse(tokenisation("(6)(7)"))
        self.assertEqual(
            tree_into_string(tree),
            "(* 6 7)"
        )
    
    def test_bare_numbers_without_operator_testing(self):
        with self.assertRaises(ValueError):
            recursive_parse(tokenisation("6 7"))
    
    def test_missing_number_testing(self):
        with self.assertRaises(ValueError):
            recursive_parse(tokenisation("+7"))
    
    def test_parenthesis_error_testing(self):
        with self.assertRaises(ValueError):
            recursive_parse(tokenisation("(6 + 7"))
    
class TestingWithSample(unittest.TestCase):
    
    def test_all_sample_cases_match(self):
        
        with open("sample_input.txt", "r", newline="") as file:
            lines = [
                line.rstrip("\r\n")
                for line in file.read().split("\n")
                if line.strip() != ""
            ]
        
        with open("sample_output.txt", "r", newline="") as file:
            blocks = file.read().replace("\r\n", "\n").strip("\n").split("\n\n")
            
        for line, block in zip(lines, blocks):
            expected = dict(entry.split(": ", 1) for entry in block.split("\n"))
            
            with self.subTest(expression=line):
                try:
                    token = tokenisation(line)
                    token_to_str = token_into_string(token)
                except ValueError:
                    token_to_str = "ERROR"
                self.assertEqual(token_to_str, expected["Tokens"])
                
                try:
                    tree = recursive_parse(token) if token_to_str != "ERROR" else None
                    tree_to_str = tree_into_string(tree) if tree is not None else "ERROR"
                except ValueError:
                    tree_to_str = "ERROR"
                self.assertEqual(tree_to_str, expected["Tree"])
                
if __name__ == "__main__":
    unittest.main()