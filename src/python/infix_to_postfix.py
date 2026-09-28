# Shunting-Yard Algorithm: Infix to Postfix (Reverse Polish Notation) Converter

from typing import List


# Splits an infix expression string into non-whitespace character tokens
def tokenize(expression: str) -> List[str]:
    return [char for char in expression if not char.isspace()]


# Converts an infix mathematical expression into a list of postfix (RPN) tokens
def infix_to_postfix(infix_expression: str) -> List[str]:
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    output: List[str] = []
    operator_stack: List[str] = []

    tokens = tokenize(infix_expression)

    for token in tokens:
        # Case 1: Operand (number or variable identifier)
        if token.isalnum():
            output.append(token)

        # Case 2: Left parenthesis -> push onto operator stack
        elif token == "(":
            operator_stack.append(token)

        # Case 3: Right parenthesis -> pop operators until matching '(' is found
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            if not operator_stack:
                raise SyntaxError("Mismatched parentheses: missing '('.")
            operator_stack.pop()  # Discard the opening parenthesis '('

        # Case 4: Arithmetic operator -> pop higher or equal precedence operators
        elif token in precedence:
            while (
                operator_stack
                and operator_stack[-1] in precedence
                and precedence[operator_stack[-1]] >= precedence[token]
            ):
                output.append(operator_stack.pop())
            operator_stack.append(token)

        else:
            raise SyntaxError(f"Unknown token encountered: '{token}'")

    # Flush all remaining operators from the stack to the output list
    while operator_stack:
        top = operator_stack.pop()
        if top == "(":
            raise SyntaxError("Mismatched parentheses: unclosed '('.")
        output.append(top)

    return output


if __name__ == "__main__":
    print("=== Infix to Postfix (Shunting-Yard) Converter ===")
    sample_infix = "(5 + 1) * (3 * 1 + 2) * (3 + 2)"
    postfix_tokens = infix_to_postfix(sample_infix)
    print(f"Infix Expression: {sample_infix}")
    print(f"Postfix Tokens:   {postfix_tokens}")
    print(f"Compact Postfix:  {''.join(postfix_tokens)}")
