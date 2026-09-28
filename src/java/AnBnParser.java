/**
 * Recursive Descent Parser for the Context-Free Grammar:
 * S -> aSb | ε
 *
 * Recognizes the formal language L = { a^n b^n | n >= 0 }.
 */
public class AnBnParser {

    private String input;
    private int pos;

    /**
     * Initializes an empty parser instance.
     */
    public AnBnParser() {
        this.input = "";
        this.pos = 0;
    }

    /**
     * Returns the lookahead character at the current cursor position without consuming it.
     *
     * @return the current character, or a sentinel space character if the end of input is reached.
     */
    private char next() {
        if (pos == input.length()) {
            return ' ';
        }
        return input.charAt(pos);
    }

    /**
     * Consumes the current character if it matches the expected terminal symbol.
     *
     * @param expected the terminal character expected by the production rule.
     * @return {@code true} if the character matches and is consumed; {@code false} otherwise.
     */
    private boolean match(char expected) {
        if (next() == expected) {
            pos++;
            return true;
        } else {
            System.out.println("  [Syntax Error] Expected '" + expected + "' at index " + pos
                    + ", but found '" + (pos < input.length() ? next() : "EOF") + "'.");
            return false;
        }
    }

    /**
     * Evaluates the non-terminal production rule: S -> aSb | ε.
     *
     * @return {@code true} if the substring conforms to production S; {@code false} otherwise.
     */
    private boolean parseS() {
        if (next() == 'a') {
            return match('a') && parseS() && match('b');
        } else {
            // Epsilon (ε) transition: returns true without advancing the cursor.
            // Any invalid trailing characters (e.g., 'c') will fail the full-consumption
            // check (pos == input.length()) inside the parse() method.
            return true;
        }
    }

    /**
     * Parses the given input string against the grammar S -> aSb | ε.
     *
     * @param text the input word to validate.
     * @return {@code true} if the entire input belongs to the language; {@code false} otherwise.
     */
    public boolean parse(String text) {
        this.input = text != null ? text : "";
        this.pos = 0;

        boolean isValidGrammar = parseS();
        if (isValidGrammar && (input.length() == pos)) {
            pos = 0;
            return true;
        } else if (isValidGrammar) {
            System.out.println("  [Syntax Error] Valid prefix in first " + pos
                    + " character(s), but unexpected trailing input remained at '"
                    + input.substring(pos) + "'.");
            pos = 0;
            return false;
        } else {
            pos = 0;
            return false;
        }
    }

    /**
     * Entry point executing demonstration test cases for the parser.
     *
     * @param args command-line arguments (optional custom strings to parse).
     */
    public static void main(String[] args) {
        AnBnParser parser = new AnBnParser();

        String[] testCases = (args.length > 0)
                ? args
                : new String[]{"aaaabbbbc", "aaabbb", "", "aaacbbb"};

        System.out.println("=== Context-Free Grammar Parser: S -> aSb | ε ===");
        for (String test : testCases) {
            String displayInput = test.isEmpty() ? "ε (empty)" : test;
            System.out.println("\nTesting input: \"" + displayInput + "\"");
            boolean result = parser.parse(test);
            System.out.println("Result for \"" + displayInput + "\": " + (result ? "ACCEPTED" : "REJECTED"));
        }
    }
}