# Stack-Based LR Postfix (Reverse Polish Notation) Expression Evaluator
#
# Context-Free Grammar for Postfix Expressions:
#   S -> K | S S O
#   K -> digit (0-9)
#   O -> '+' | '-' | '*' | '/'

from typing import Sequence, Union


# Applies a binary arithmetic operator to two numeric operands
def calculate(
    left: Union[int, float], operator: str, right: Union[int, float]
) -> float:
    left_val = float(left)
    right_val = float(right)

    if operator == "+":
        return left_val + right_val
    if operator == "-":
        return left_val - right_val
    if operator == "*":
        return left_val * right_val
    if operator == "/":
        return left_val / right_val
    raise ValueError(f"Unknown operator: '{operator}'")


# Evaluates a sequence of postfix tokens using an explicit operand stack
def evaluate_postfix(expression_tokens: Sequence[str]) -> float:
    stack: list[float] = []

    for token in expression_tokens:
        if token.isdigit():
            stack.append(float(token))
        elif token in ("+", "-", "*", "/"):
            if len(stack) < 2:
                raise ValueError(
                    f"Insufficient operands on stack for operator '{token}'."
                )
            right = stack.pop()
            left = stack.pop()
            result = calculate(left, token, right)
            stack.append(result)
        else:
            raise ValueError(f"Invalid token in postfix expression: '{token}'")

    if len(stack) != 1:
        raise ValueError(
            "Malformed postfix expression: stack does not contain a single result."
        )

    return stack.pop()


if __name__ == "__main__":
    # Example: (x + 1) * (3 * y + 2) * (z + 2)
    # Postfix form: x 1 + 3 y * 2 + * z 2 + *
    # With x = 5, y = 1, z = 3 => 6 * (3 + 2) * 5 = 150.0
    postfix_expression = "51+31*2+*32+*"

    print("=== LR Postfix Stack Evaluator ===")
    print(f"Postfix Expression: {postfix_expression}")
    print(f"Evaluated Result:   {evaluate_postfix(postfix_expression)}")
