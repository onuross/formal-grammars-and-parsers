# LL(1) Recursive Descent Parsers for Four Formal Grammars
#
# Implements predictive parsing using Python Structural Pattern Matching:
#   Grammar (a): S -> aSa | bSb | x
#   Grammar (b): S -> aSb | epsilon
#   Grammar (c): S -> (S)S | epsilon
#   Grammar (d): S -> ABc,  A -> aA | epsilon,  B -> bB | epsilon

from typing import Optional


class LL1Parser:
    # Initializes the LL(1) parser with input text and cursor index
    def __init__(self, text: str) -> None:
        self.input_text: str = text
        self.pos: int = 0

    # Returns the current lookahead character, or None if at the end of input
    def current_char(self) -> Optional[str]:
        if self.pos < len(self.input_text):
            return self.input_text[self.pos]
        return None

    # Consumes the current character if it matches the expected terminal symbol
    def match(self, expected_char: str) -> bool:
        if self.current_char() == expected_char:
            self.pos += 1
            return True
        return False

    # Helper method to run a specific grammar start symbol and verify full input consumption
    def _run_parser(self, rule_method) -> bool:
        self.pos = 0
        is_valid = rule_method()
        # Accept if the grammar rule succeeded and all characters (or optional '$' EOF marker) were consumed
        remaining = self.current_char()
        return is_valid and (
            remaining is None
            or (remaining == "$" and self.pos == len(self.input_text) - 1)
        )

    # -------------------------------------------------------------------------
    # Grammar (a): S -> aSa | bSb | x
    # -------------------------------------------------------------------------
    def parse_s_a(self) -> bool:
        char = self.current_char()
        match char:
            case "a":  # S -> aSa
                return self.match("a") and self.parse_s_a() and self.match("a")
            case "b":  # S -> bSb
                return self.match("b") and self.parse_s_a() and self.match("b")
            case "x":  # S -> x
                return self.match("x")
            case _:
                return False

    # -------------------------------------------------------------------------
    # Grammar (b): S -> aSb | epsilon
    # -------------------------------------------------------------------------
    def parse_s_b(self) -> bool:
        char = self.current_char()
        match char:
            case "a":  # S -> aSb
                return self.match("a") and self.parse_s_b() and self.match("b")
            case "b" | "\(" | None:  # S -> epsilon (FOLLOW(S) = {'b', '\)', EOF})
                return True
            case _:
                return False

    # -------------------------------------------------------------------------
    # Grammar (c): S -> (S)S | epsilon (Dyck Language of balanced parentheses)
    # -------------------------------------------------------------------------
    def parse_s_c(self) -> bool:
        char = self.current_char()
        match char:
            case "(":  # S -> (S)S
                return (
                    self.match("(")
                    and self.parse_s_c()
                    and self.match(")")
                    and self.parse_s_c()
                )
            case ")" | "\(" | None:  # S -> epsilon (FOLLOW(S) = {')', '\)', EOF})                
                return True
            case _:
                return False

    # -------------------------------------------------------------------------
    # Grammar (d): S -> ABc,  A -> aA | epsilon,  B -> bB | epsilon
    # -------------------------------------------------------------------------
    def parse_s_d(self) -> bool:
        char = self.current_char()
        match char:
            case "a" | "b" | "c":  # FIRST(ABc) = {'a', 'b', 'c'}
                return self.parse_a_d() and self.parse_b_d() and self.match("c")
            case _:
                return False

    def parse_a_d(self) -> bool:
        char = self.current_char()
        match char:
            case "a":  # A -> aA
                return self.match("a") and self.parse_a_d()
            case "b" | "c":  # A -> epsilon (FOLLOW(A) = {'b', 'c'})
                return True
            case _:
                return False

    def parse_b_d(self) -> bool:
        char = self.current_char()
        match char:
            case "b":  # B -> bB
                return self.match("b") and self.parse_b_d()
            case "c":  # B -> epsilon (FOLLOW(B) = {'c'})
                return True
            case _:
                return False


if __name__ == "__main__":
    print("=== LL(1) Predictive Parsers Demonstration ===")

    test_suite = [
        ("Grammar (a) [S -> aSa | bSb | x]", "abxba", "parse_s_a"),
        ("Grammar (a) [S -> aSa | bSb | x]", "abxab", "parse_s_a"),
        ("Grammar (b) [S -> aSb | eps]", "aaabbb", "parse_s_b"),
        ("Grammar (b) [S -> aSb | eps]", "aaabb", "parse_s_b"),
        ("Grammar (c) [S -> (S)S | eps]", "(()())()", "parse_s_c"),
        ("Grammar (c) [S -> (S)S | eps]", "(()()", "parse_s_c"),
        ("Grammar (d) [S -> ABc]", "aaabbc", "parse_s_d"),
        ("Grammar (d) [S -> ABc]", "c", "parse_s_d"),
    ]

    for label, word, method_name in test_suite:
        parser = LL1Parser(word)
        rule_fn = getattr(parser, method_name)
        accepted = parser._run_parser(rule_fn)
        status = "ACCEPTED" if accepted else "REJECTED"
        print(f"{label:35} | Input: {word!r:10} -> {status}")
