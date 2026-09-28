# Recursive Abstract Syntax Tree (AST) Evaluator
#
# Evaluates nested list AST structures produced by ASTParser:
#   - Numeric leaf: int or float
#   - Unary node:   ['sqrt()', X] or ['exp()', X]
#   - Binary node:  [op, X, Y] where op is in {'+', '-', '*', '/', '^'}

import math
from typing import Any


def evaluate_ast(node: Any) -> float:
    # Base case: node is already an integer or floating-point number
    if isinstance(node, (int, float)):
        return float(node)

    if not isinstance(node, list):
        raise SyntaxError(f"Invalid AST node type: {type(node).__name__}")

    # Unary operator node: ['sqrt()', X] or ['exp()', X]
    if len(node) == 2:
        operator = node[0]
        operand = evaluate_ast(node[1])
        if operator == "sqrt()":
            return math.pow(operand, 0.5)
        if operator == "exp()":
            return math.exp(operand)
        raise SyntaxError(f"Unknown unary operator: {operator}")

    # Binary operator node: [op, X, Y] where op in {'+', '-', '*', '/', '^'}
    if len(node) == 3:
        operator = node[0]
        operand1 = evaluate_ast(node[1])
        operand2 = evaluate_ast(node[2])
        if operator == "+":
            return operand1 + operand2
        if operator == "-":
            return operand1 - operand2
        if operator == "*":
            return operand1 * operand2
        if operator == "/":
            return operand1 / operand2
        if operator == "^":
            return operand1**operand2
        raise SyntaxError(f"Unknown binary operator: {operator}")

    raise SyntaxError(f"Malformed AST node structure: {node}")


if __name__ == "__main__":
    print("=== AST Evaluator Demonstration ===")

    valid_ast = ["+", ["sqrt()", 16.0], ["exp()", 0.0]]
    print(f"Evaluating {valid_ast} -> {evaluate_ast(valid_ast)}")

    # Demonstrating syntax error handling on a malformed AST node (arity = 1)
    malformed_ast = [["sqrt()", 16.0]]
    try:
        print(evaluate_ast(malformed_ast))
    except SyntaxError as err:
        print(f"Expected SyntaxError caught for {malformed_ast}: {err}")
