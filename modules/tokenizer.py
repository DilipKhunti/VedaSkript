import re

class Tokenizer:
    
    def __init__(self, code, debug=False):
        self.code = code
        self.debug = debug
    
    # Define token types and their patterns
    TOKENS = [
        ("COMMENT", r"//[^\n]*|/\*.*?\*/"),  # Single-line and multi-line comments
        ("KEYWORD", r"कार्य मुख्यः|चरः|मुद्रणम्|यदि|अन्यथा यदि|अन्यथा|यावद्‌|अनुवर्तते|विरमतु|कार्य|प्रतिददाति"),  # Keywords
        ("LOGICAL_OPERATOR", r"&&|\|\|"),  # Logical operators (AND, OR)
        ("BINARY_OPERATOR", r"==|<=|>=|<|>|!="),  # Comparison operators
        ("ASSIGNMENT_OPERATOR", r"=|\+=|-=|\*=|/=|%="),  # Assignment operators
        ("BINARY_OPERATOR", r"\+|-|\*|/|%"),  # Arithmetic operators
        ("BOOLEAN", r"सत्य|असत्य"),  # Boolean literals
        ("NULL", r"रिक्त"),  # Null literal
        ("IDENTIFIER", r"[अ-हa-zA-Z\u0900-\u097F]+(?:[अ-हa-zA-Z0-9_])*"),  # Identifiers (including Devanagari characters)
        ("FLOAT", r"[0-9]+\.[0-9]+"),  # Floating-point numbers
        ("NUMBER", r"[0-9]+"),  # Integer numbers
        ("STRING", r"\"(\\.|[^\\\"])*\""),  # String literals
        ("PUNCTUATION", r"[{}();,]"),  # Punctuation characters
        ("WHITESPACE", r"\s+"),  # Whitespace (spaces, tabs, newlines)
    ]

    # Pre-compile all token patterns for performance
    TOKEN_REGEX = [(token_type, re.compile(pattern, re.DOTALL)) for token_type, pattern in TOKENS]

    def tokenize(self):
        """
        Tokenizes the input self.code into a list of tokens.

        :param self.code: The input self.code as a string.
        :param self.debug: If True, prints self.debug information during tokenization.
        :return: A list of (token_type, value, line, column) tuples.
        """
        tokens = []
        line = 1
        column = 1

        while self.code:
            match = None
            for token_type, regex in Tokenizer.TOKEN_REGEX:
                match = regex.match(self.code)
                if match:
                    value = match.group(0)

                    # Handle comments: skip adding them to the token list
                    if token_type == "COMMENT":
                        if self.debug:
                            print(f"Ignored {token_type}: '{value}' at line {line}, column {column}")

                    # Handle other token types: add them to the token list (skip whitespace)
                    elif token_type != "WHITESPACE":
                        tokens.append((token_type, value, line, column))

                    if self.debug and token_type != "COMMENT":
                        print(f"Matched {token_type}: '{value}' at line {line}, column {column}")

                    # Update self.code, column, and line positions
                    self.code = self.code[match.end():]
                    column += match.end()

                    # Adjust line and column for multi-line tokens
                    if '\n' in value:
                        line += value.count('\n')
                        column = len(value.split('\n')[-1]) + 1
                    break

            # Raise an error if no token matches the current self.code
            if not match:
                return {"type":"TokenizerOutput",
                        "response": False,
                        "message": f"Unexpected character '{self.code[0]}' at line {line}, column {column}",
                        "tokens": []}


        return {"type":"TokenizerOutput",
                "response": True,
                "message": f"Tokenization successful.",
                "tokens": tokens}
