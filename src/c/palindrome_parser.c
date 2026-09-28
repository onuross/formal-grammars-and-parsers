/**
 * @file palindrome_parser.c
 * @brief Recursive Descent Parser for center-marked palindromes over {a, b, c}.
 *
 * Grammar Definition:
 *   S -> aSa | bSb | cSc | x
 *
 * Recognizes the language L = { w x w^R | w in {a, b, c}* }.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stddef.h>

static const char *input = NULL;
static size_t pos = 0;

/**
 * @brief Returns the character at the current position without advancing the cursor.
 * @return Current lookahead character (or '\0' at end of string).
 */
static char next(void) {
    return input[pos];
}

/**
 * @brief Matches and consumes the expected terminal symbol.
 * @param expected The expected character.
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
 * @brief Evaluates the production rule S -> aSa | bSb | cSc | x.
 * @return true if the derivation succeeds, false otherwise.
 */
static bool parse_s(void) {
    if (next() == 'a') {
        return match('a') && parse_s() && match('a');
    } else if (next() == 'b') {
        return match('b') && parse_s() && match('b');
    } else if (next() == 'c') {
        return match('c') && parse_s() && match('c');
    } else if (next() == 'x') {
        return match('x'); /* Center marker of the palindrome */
    } else {
        return false;
    }
}

/**
 * @brief Validates whether a given null-terminated string belongs to the grammar.
 * @param text Input string to parse.
 * @return true if syntax is valid and the entire word is consumed, false otherwise.
 */
bool parse_palindrome(const char *text) {
    if (text == NULL) {
        return false;
    }
    input = text;
    pos = 0;

    bool syntax_ok = parse_s();
    /* Ensure the entire input word has been consumed (matches end of line or null terminator) */
    bool is_eof = (next() == '\0' || match('\n'));
    return syntax_ok && is_eof && (next() == '\0');
}

/**
 * @brief Main entry point supporting CLI arguments, interactive mode (--interactive), and demo suite.
 */
int main(int argc, char *argv[]) {
    if (argc > 1 && strcmp(argv[1], "--interactive") == 0) {
        char buf[128];
        printf("Input: ");
        if (fgets(buf, sizeof(buf), stdin) == NULL) {
            fprintf(stderr, "Error reading input.\n");
            return EXIT_FAILURE;
        }

        if (parse_palindrome(buf)) {
            printf("Syntax correct!\n");
            return EXIT_SUCCESS;
        } else {
            printf("Wrong Syntax!\n");
            return EXIT_FAILURE;
        }
    }

    const char *test_cases[] = {"abxcba", "abcxcba", "x", "abxba", "abxcba_extra"};
    size_t num_tests = sizeof(test_cases) / sizeof(test_cases[0]);

    printf("=== Palindrome Grammar Parser (S -> aSa | bSb | cSc | x) ===\n");
    for (size_t i = 0; i < num_tests; i++) {
        bool valid = parse_palindrome(test_cases[i]);
        printf("Input: %-15s -> %s\n", test_cases[i], valid ? "ACCEPTED (Syntax correct)" : "REJECTED (Wrong Syntax)");
    }

    return EXIT_SUCCESS;
}