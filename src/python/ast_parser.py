# Abstract Syntax Tree (AST) Recursive Descent Parser
#
# Grammar Rules:
#   K -> M { ('+' | '-') M }          (Left-associative AST node: [op, left, right])
#   M -> P { ('*' | '/') P }          (Left-associative AST node: [op, left, right])
#   P -> S [ '^' P ]                  (Right-associative AST node: ['^', base, power])
#   S -> number | 'x' | '(' K ')' | 'sqrt(' K ')' | 'exp(' K ')'

from typing import List, Optional, Union

# Recursive type alias for AST nodes: float, variable 'x', or nested operator lists
ASTNode = Union[float, str, List["ASTNode"]]


class ASTParser:
    # Initializes the AST parser with input expression text and cursor index
    def __init__(self, text: str) -> None:
        self.input_text: str = text
        self.pos: int = 0

    # Returns the character at the current position without advancing the cursor
    def current_char(self) -> Optional[str]:
        if self.pos < len(self.input_text):
            return self.input_text[self.pos]
        return None

    # Advances the cursor position by one character
    def step(self) -> None:
        self.pos += 1

    # Skips consecutive space characters in the input
    def skip_whitespace(self) -> None:
        while self.current_char() is not None and self.current_char() == " ":
            self.step()

    # Parses an integer or floating-point number into a float leaf node
    def parse_number(self) -> float:
        result = ""
        while self.current_char() is not None and (
            self.current_char().isdigit() or self.current_char() == "."
        ):
            result += self.current_char()
            self.step()
        try:
            return float(result)
        except ValueError as exc:
            raise SyntaxError(f"Malformed number literal: '{result}'") from exc

    # Parses an alphabetic identifier (functions 'sqrt', 'exp', or variable 'x')
    def parse_identifier(self) -> str:
        result = ""
        while self.current_char() is not None and self.current_char().isalpha():
            result += self.current_char()
            self.step()
        return result

    # Production K: Addition and Subtraction -> builds left-associative tree [op, left, right]
    def parse_k(self) -> ASTNode:
        result: ASTNode = self.parse_m()
        self.skip_whitespace()
        char = self.current_char()
        while char in ("+", "-"):
            self.step()
            operand = self.parse_m()
            self.skip_whitespace()
            result = [char, result, operand]
            char = self.current_char()
        return result

    # Production M: Multiplication and Division -> builds left-associative tree [op, left, right]
    def parse_m(self) -> ASTNode:
        result: ASTNode = self.parse_p()
        self.skip_whitespace()
        char = self.current_char()
        while char in ("*", "/"):
            self.step()
            operand = self.parse_p()
            self.skip_whitespace()
            result = [char, result, operand]
            char = self.current_char()
        return result

    # Production P: Exponentiation -> builds right-associative tree ['^', base, power]
    def parse_p(self) -> ASTNode:
        result: ASTNode = self.parse_s()
        self.skip_whitespace()
        char = self.current_char()
        if char == "^":
            self.step()
            self.skip_whitespace()
            power = self.parse_p()
            result = [char, result, power]
        return result

    # Production S: Numbers, variable 'x', parentheses, sqrt(K), and exp(K)
    def parse_s(self) -> ASTNode:
        self.skip_whitespace()
        char = self.current_char()

        if char is None:
            raise SyntaxError("Unexpected end of input while parsing factor.")

        if char.isdigit():
            return self.parse_number()

        if char == "(":
            self.step()
            inside = self.parse_k()
            self.skip_whitespace()
            if self.current_char() != ")":
                raise SyntaxError("Missing closing parenthesis ')'.")
            self.step()
            return inside

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
                    raise SyntaxError("Wrong parenthesis structure in 'sqrt'.")
                self.step()
                return ["sqrt()", inside]
            if word == "exp":
                if self.current_char() != "(":
                    raise SyntaxError("Expected '(' after 'exp'.")
                self.step()
                inside = self.parse_k()
                self.skip_whitespace()
                if self.current_char() != ")":
                    raise SyntaxError("Wrong parenthesis structure in 'exp'.")
                self.step()
                return ["exp()", inside]
            if word == "x":
                # Symbolic variable leaf node used by the symbolic differentiator
                return "x"
            raise SyntaxError(f"Unknown identifier: '{word}'.")

        raise SyntaxError(f"Unexpected character '{char}' at index {self.pos}.")

    # Parses the entire input expression and returns the root AST node
    def parse(self) -> ASTNode:
        self.pos = 0
        tree = self.parse_k()
        self.skip_whitespace()
        if self.current_char() is not None:
            raise SyntaxError(
                f"Unexpected trailing character '{self.current_char()}' at index {self.pos}."
            )
        return tree


if __name__ == "__main__":
    print("=== Abstract Syntax Tree (AST) Parser ===")

    # Test 1: 16 + 8 / 4 * 2
    parser1 = ASTParser("16 +   8/   4*    2")
    print("Test 1 AST:", parser1.parse())

    # Test 2: 2 ^ 3 ^ 2 (Right-associative)
    parser2 = ASTParser("2 ^     3   ^    2")
    print("Test 2 AST:", parser2.parse())

    # Test 3: sqrt(16) + exp(0)
    parser3 = ASTParser("sqrt(   16) +      exp(0   )")
    print("Test 3 AST:", parser3.parse())
