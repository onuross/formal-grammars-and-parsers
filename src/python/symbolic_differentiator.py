# Symbolic Differentiation Engine over Abstract Syntax Trees (AST)
#
# Computes the formal derivative d/dx of mathematical expressions using
# Python Structural Pattern Matching (match / case).

from ast_parser import ASTNode, ASTParser


# Computes the symbolic derivative of the given AST node with respect to 'x'
def differentiate(ast: ASTNode) -> ASTNode:
    match ast:
        # Constant rule: d/dx (c) = 0
        case float() | int():
            return 0

        # Identity variable rule: d/dx (x) = 1
        case "x":
            return 1

        # Sum rule: (u + v)' = u' + v'
        case ["+", u, v]:
            return ["+", differentiate(u), differentiate(v)]

        # Difference rule: (u - v)' = u' - v'
        case ["-", u, v]:
            return ["-", differentiate(u), differentiate(v)]

        # Product rule: (u * v)' = u' * v + v' * u
        case ["*", u, v]:
            return ["+", ["*", differentiate(u), v], ["*", differentiate(v), u]]

        # Quotient rule: (u / v)' = (u' * v - v' * u) / (v * v)
        case ["/", u, v]:
            return [
                "/",
                ["-", ["*", differentiate(u), v], ["*", differentiate(v), u]],
                ["*", v, v],
            ]

    # Raise an error if the AST node does not match any supported differentiation rule
    raise SyntaxError(f"Unsupported AST node for differentiation: {ast}")


if __name__ == "__main__":
    expression_str = "3 * x * ( 2 * x + 1 ) + 5"
    parser = ASTParser(expression_str)
    expression_ast = parser.parse()
    derivative_ast = differentiate(expression_ast)

    print("=== Symbolic Differentiation Engine ===")
    print(f"Expression:     {expression_str}")
    print(f"Expression AST: {expression_ast}")
    print(f"Derivative AST: {derivative_ast}")
