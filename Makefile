# ==============================================================================
# Polyglot Build & Test Automation (C99, Java, Python 3)
# ==============================================================================

CC          := gcc
CFLAGS      := -std=c99 -Wall -Wextra -Wpedantic -O2
LDFLAGS     := -lm

JAVAC       := javac
JAVA        := java
PYTHON      := python3

C_SRC_DIR   := src/c
JAVA_SRC_DIR:= src/java
PY_SRC_DIR  := src/python
BUILD_DIR   := build

C_BINS      := $(BUILD_DIR)/c/palindrome_parser $(BUILD_DIR)/c/expression_parser
JAVA_CLASS  := $(BUILD_DIR)/java/AnBnParser.class

.PHONY: all build build-c build-java test test-c test-java test-python clean help

# Default target: compile C and Java modules, then run all polyglot test suites
all: build test

# ------------------------------------------------------------------------------
# Build Targets
# ------------------------------------------------------------------------------
build: build-c build-java

build-c: $(C_BINS)

$(BUILD_DIR)/c/palindrome_parser: $(C_SRC_DIR)/palindrome_parser.c
	@mkdir -p $(BUILD_DIR)/c
	$(CC) $(CFLAGS) $(C_SRC_DIR)/palindrome_parser.c -o $(BUILD_DIR)/c/palindrome_parser

$(BUILD_DIR)/c/expression_parser: $(C_SRC_DIR)/expression_parser.c
	@mkdir -p $(BUILD_DIR)/c
	$(CC) $(CFLAGS) $(C_SRC_DIR)/expression_parser.c -o $(BUILD_DIR)/c/expression_parser $(LDFLAGS)

build-java: $(JAVA_CLASS)

$(JAVA_CLASS): $(JAVA_SRC_DIR)/AnBnParser.java
	@mkdir -p $(BUILD_DIR)/java
	$(JAVAC) -d $(BUILD_DIR)/java $(JAVA_SRC_DIR)/AnBnParser.java

# ------------------------------------------------------------------------------
# Test / Demo Execution Targets
# ------------------------------------------------------------------------------
test: test-c test-java test-python

test-c: build-c
	@echo "\n================ [C99 MODULES] ================"
	./$(BUILD_DIR)/c/palindrome_parser
	@echo ""
	./$(BUILD_DIR)/c/expression_parser

test-java: build-java
	@echo "\n================ [JAVA MODULE] ================"
	$(JAVA) -cp $(BUILD_DIR)/java AnBnParser

test-python:
	@echo "\n=============== [PYTHON MODULES] ==============="
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/expression_parser.py
	@echo ""
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/ast_parser.py
	@echo ""
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/ast_evaluator.py
	@echo ""
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/symbolic_differentiator.py
	@echo ""
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/infix_to_postfix.py
	@echo ""
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/postfix_evaluator.py
	@echo ""
	PYTHONPATH=$(PY_SRC_DIR) $(PYTHON) $(PY_SRC_DIR)/ll1_parsers.py

# ------------------------------------------------------------------------------
# Housekeeping
# ------------------------------------------------------------------------------
clean:
	rm -rf $(BUILD_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.class" -delete
	find . -type f -name "*.o" -delete

help:
	@echo "Available targets:"
	@echo "  make all          - Build C/Java modules and execute all tests (C, Java, Python)"
	@echo "  make build        - Compile C99 binaries and Java bytecode into ./build"
	@echo "  make test         - Run all demonstration and validation suites"
	@echo "  make test-c       - Run C99 parser demos only"
	@echo "  make test-java    - Run Java parser demo only"
	@echo "  make test-python  - Run Python parser & AST demos only"
	@echo "  make clean        - Remove build artifacts and cache directories"