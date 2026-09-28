/**
 * @file expression_parser.c
 * @brief Recursive Descent Parser and Evaluator for Mathematical Expressions.
 *
 * Context-Free Grammar (with operator precedence and associativity):
 *   K -> M { ('+' | '-') M }          (Addition / Subtraction, left-associative)
 *   M -> P { ('*' | '/') P }          (Multiplication / Division, left-associative)
 *   P -> S [ '^' P ]                  (Exponentiation, right-associative)
 *   S -> number | '(' K ')' | 'sqrt(' K ')' | 'exp(' K ')'
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <math.h>


static const char *input = NULL;
static size_t pos = 0;
static bool has_syntax_error = false;

/* Forward declarations of grammar production functions */
static double parse_k(void);
static double parse_m(void);
static double parse_p(void);
static double parse_s(void);

/**
 * @brief Skips whitespace and returns the current lookahead character.
 * @return Next non-whitespace character, or '\0' at end of string.
 */
static char next(void) {
    while (input[pos] == ' ' || input[pos] == '\t') {
        pos++;
    }
    return input[pos];
}

/**
 * @brief Matches and consumes the expected character after skipping whitespace.
 * @param expected The terminal symbol to match.
 * @return true if matched and consumed, false otherwise.
 */
static bool match(char expected) {
    if (next() == expected) {
        pos++;
        return true;
    }
    return false;
}

/**
 * @brief Production S: Parses numbers, parenthesized expressions, sqrt(K), and exp(K).
 * @return Evaluated numeric result of the factor.
 */
static double parse_s(void) {
    if (has_syntax_error) {
        return 0.0;
    }

    /* Skip leading whitespace before attempting numeric conversion */
    next();

    char *end_ptr = NULL;
    double double_value = strtod(&input[pos], &end_ptr);

    if (end_ptr != &input[pos] && input[pos] != '+' && input[pos] != '-') {
        pos = (size_t)(end_ptr - input);
        return double_value;
    }

    if (next() == '(') {
        match('(');
        double value = parse_k();
        if (!match(')')) {
            has_syntax_error = true;
        }
        return value;
    } else if (next() == 's') {
        if (match('s') && match('q') && match('r') && match('t') && match('(')) {
            double value = pow(parse_k(), 0.5);
            if (!match(')')) {
                has_syntax_error = true;
            }
            return value;
        }
        has_syntax_error = true;
        return 0.0;
    } else if (next() == 'e') {
        if (match('e') && match('x') && match('p') && match('(')) {
            double value = exp(parse_k());
            if (!match(')')) {
                has_syntax_error = true;
            }
            return value;
        }
        has_syntax_error = true;
        return 0.0;
    } else {
        has_syntax_error = true;
        return 0.0;
    }
}

/**
 * @brief Production P: Exponentiation (Right-associative: P -> S [^ P]).
 * @return Evaluated numeric result.
 */
static double parse_p(void) {
    double value = parse_s();
    if (next() == '^') {
        match('^');
        value = pow(value, parse_p());
    }
    return value;
}

/**
 * @brief Production M: Multiplication and Division (Left-associative: M -> P { (* | /) P }).
 * @return Evaluated numeric result.
 */
static double parse_m(void) {
    double value = parse_p();
    while (next() == '*' || next() == '/') {
        if (next() == '*') {
            match('*');
            value *= parse_p();
        } else {
            match('/');
            value /= parse_p();
        }
    }
    return value;
}

/**
 * @brief Production K: Addition and Subtraction (Left-associative: K -> M { (+ | -) M }).
 * @return Evaluated numeric result.
 */
static double parse_k(void) {
    double value = parse_m();
    while (next() == '-' || next() == '+') {
        if (next() == '-') {
            match('-');
            value -= parse_m();
        } else {
            match('+');
            value += parse_m();
        }
    }
    return value;
}

/**
 * @brief Parses and evaluates a mathematical expression string.
 * @param expr Null-terminated expression string.
 * @param out_result Pointer to store the evaluated result.
 * @return true if parsing succeeded without syntax errors, false otherwise.
 */
bool evaluate_expression(const char *expr, double *out_result) {
    if (expr == NULL || out_result == NULL) {
        return false;
    }
    input = expr;
    pos = 0;
    has_syntax_error = false;

    double calc = parse_k();
    bool is_eof = (next() == '\0' || match('\n'));

    if (!has_syntax_error && is_eof && next() == '\0') {
        *out_result = calc;
        return true;
    }
    return false;
}

/**
 * @brief Main entry point running demonstration expressions or interactive stdin mode.
 */
int main(int argc, char *argv[]) {
    if (argc > 1 && strcmp(argv[1], "--interactive") == 0) {
        char buf[128];
        printf("Input: ");
        if (fgets(buf, sizeof(buf), stdin) == NULL) {
            fprintf(stderr, "Error reading input.\n");
            return EXIT_FAILURE;
        }

        double result = 0.0;
        if (evaluate_expression(buf, &result)) {
            printf("Syntax correct and result is: %f\n", result);
            return EXIT_SUCCESS;
        } else {
            printf("Wrong Syntax!\n");
            return EXIT_FAILURE;
        }
    }

    const char *test_expressions[] = {
        "16 + 8 / 4 * 2",
        "2 ^ 3 ^ 2",
        "sqrt(16) + exp(0)",
        "(2 + 3) * 4 ^ 2"
    };
    size_t num_tests = sizeof(test_expressions) / sizeof(test_expressions[0]);

    printf("=== Arithmetic Expression Parser & Evaluator (C99) ===\n");
    for (size_t i = 0; i < num_tests; i++) {
        double result = 0.0;
        if (evaluate_expression(test_expressions[i], &result)) {
            printf("Expression: %-22s -> Result: %.4f\n", test_expressions[i], result);
        } else {
            printf("Expression: %-22s -> SYNTAX ERROR\n", test_expressions[i]);
        }
    }

    return EXIT_SUCCESS;
}