# Recursive Descent Parser and Evaluator for Arithmetic Expressions
#
# Grammar Rules:
#   K -> M { ('+' | '-') M }          (Addition / Subtraction, left-associative)
#   M -> P { ('*' | '/') P }          (Multiplication / Division, left-associative)
#   P -> S [ '^' P ]                  (Exponentiation, right-associative)
#   S -> number | '(' K ')' | 'sqrt(' K ')' | 'exp(' K ')'

import math
from typing import Optional


class ExpressionParser:
    # Initializes the parser with the input expression string and cursor position
    def __init__(self, text: str) -> None:
        self.input_text: str = text
        self.pos: int = 0

    # Returns the character at the current cursor position without advancing
    def current_char(self) -> Optional[str]:
        if self.pos < len(self.input_text):
            return self.input_text[self.pos]
        return None

    # Advances the input cursor by one character
    def step(self) -> None:
        self.pos += 1

    # Skips consecutive whitespace characters
    def skip_whitespace(self) -> None:
        while self.current_char() is not None and self.current_char() == " ":
            self.step()

    # Parses an integer or floating-point number literal
    def parse_number(self) -> float:
        result = ""
        # Continue while the current character is a digit or a decimal point
        while self.current_char() is not None and (
            self.current_char().isdigit() or self.current_char() == "."
        ):
            result += self.current_char()
            self.step()
        try:
            return float(result)
        except ValueError as exc:
            raise SyntaxError(f"Malformed numeric literal: '{result}'") from exc

    # Parses alphabetic function identifiers such as 'sqrt' and 'exp'
    def parse_identifier(self) -> str:
        result = ""
        while self.current_char() is not None and self.current_char().isalpha():
            result += self.current_char()
            self.step()
        return result

    # Each grammar method calls the next higher-precedence production rule

    # Production K: Addition and Subtraction -> K -> M { ('+' | '-') M }
    def parse_k(self) -> float:
        result = self.parse_m()
        self.skip_whitespace()
        char = self.current_char()
        while char in ("+", "-"):
            self.step()
            operand = self.parse_m()
            self.skip_whitespace()
            if char == "+":
                result += operand
            else:
                result -= operand
            char = self.current_char()
        return result

    # Production M: Multiplication and Division -> M -> P { ('*' | '/') P }
    def parse_m(self) -> float:
        result = self.parse_p()
        self.skip_whitespace()
        char = self.current_char()
        while char in ("*", "/"):
            self.step()
            operand = self.parse_p()
            self.skip_whitespace()
            if char == "*":
                result *= operand
            else:
                result /= operand
            char = self.current_char()
        return result

    # Production P: Exponentiation -> P -> S [ '^' P ] (Right-associative)
    def parse_p(self) -> float:
        base = self.parse_s()
        self.skip_whitespace()
        char = self.current_char()
        if char == "^":
            self.step()
            self.skip_whitespace()
            power = self.parse_p()
            return base**power  # P -> S ^ P
        return base  # P -> S

    # Production S: Numbers, Parentheses, sqrt(K), and exp(K)
    def parse_s(self) -> float:
        self.skip_whitespace()
        char = self.current_char()

        if char is None:
            raise SyntaxError("Unexpected end of input while expecting a factor.")

        # Case 1: Numeric literal
        if char.isdigit():
            return self.parse_number()

        # Case 2: Parenthesized sub-expression (K)
        if char == "(":
            self.step()
            inside = self.parse_k()
            self.skip_whitespace()
            if self.current_char() != ")":
                raise SyntaxError("Missing closing parenthesis ')'.")
            self.step()
            return inside

        # Case 3: Built-in mathematical functions sqrt(K) and exp(K)
        if char.isalpha():
            word = self.parse_identifier()
            self.skip_whitespace()
            if word == "sqrt":
                if self.current_char() != "(":
                    raise SyntaxError("Expected '(' after 'sqrt'.")
                self.step()
                inside = self.parse_k()
                self.skip_whitespace()
                if self.current_char() != ")":
                    raise SyntaxError("Missing closing parenthesis ')' for 'sqrt'.")
                self.step()
                return math.pow(inside, 0.5)
            if word == "exp":
                if self.current_char() != "(":
                    raise SyntaxError("Expected '(' after 'exp'.")
                self.step()
                inside = self.parse_k()
                self.skip_whitespace()
                if self.current_char() != ")":
                    raise SyntaxError("Missing closing parenthesis ')' for 'exp'.")
                self.step()
                return math.exp(inside)
            raise SyntaxError(f"Unknown function identifier: '{word}'.")

        raise SyntaxError(f"Unexpected token '{char}' at position {self.pos}.")

    # Parses the entire input and verifies no unconsumed characters remain
    def evaluate(self) -> float:
        self.pos = 0
        result = self.parse_k()
        self.skip_whitespace()
        if self.current_char() is not None:
            raise SyntaxError(
                f"Unexpected trailing character '{self.current_char()}' at position {self.pos}."
            )
        return result


if __name__ == "__main__":
    # Test 1: 16 + 8 / 4 * 2 = 16 + 2 * 2 = 20.0
    parser1 = ExpressionParser("16 +   8/   4*    2")
    print("Test 1:", parser1.evaluate())

    # Test 2: 2 ^ 3 ^ 2 = 2 ^ 9 = 512.0 (Right-associative exponentiation)
    parser2 = ExpressionParser("2 ^     3   ^    2")
    print("Test 2:", parser2.evaluate())

    # Test 3: sqrt(16) + exp(0) = 4.0 + 1.0 = 5.0
    parser3 = ExpressionParser("sqrt(   16) +      exp(0   )")
    print("Test 3:", parser3.evaluate())
