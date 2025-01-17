class Parser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.pos = 0
        self.debug = debug

    def current(self):
        # Return the current token if within bounds, else None
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token_type=None):
        # Consume and return the current token, optionally verifying its type
        token = self.current()

        if self.debug:
            print(f"Consuming token: {token}")

        if token is None:
            raise SyntaxError("Unexpected end of input")
        if token_type and token[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token[0]}, value = '{token[1]}' at line {token[2]} column {token[3]}")

        self.pos += 1
        return token

    def parse_program(self):
        # Parse the program as a series of statements
        body = []

        try:
            while self.current():
                statement = self.parse_statement()
                if statement:
                    body.append(statement)
        except SyntaxError as e:
            return {"type" : "ParserOutput", "response": False, "message": str(e), "AST" : {"type": "SanskritProgram", "body": []}}

        return {"type" : "ParserOutput", "response": True, "message": "Parsing successful.", "AST" : {"type": "SanskritProgram", "body": body}}

    def parse_statement(self):
        # Determine the type of statement and parse accordingly
        token = self.current()
        if token and token[0] == "KEYWORD":
            keyword = token[1]
            if keyword == "कार्य मुख्यः":
                return self.parse_main_function()
            elif keyword == "कार्य":
                return self.parse_function_defination()
            elif keyword == "प्रतिददाति":
                return self.parse_return_statement()
            elif keyword == "चरः":
                return self.parse_variable_declaration()
            elif keyword == "मुद्रणम्":
                return self.parse_print_statement()
            elif keyword == "यदि":
                return self.parse_if_statement()
            elif keyword == "यावद्‌":
                return self.parse_while_statement()
            elif keyword == "विरमतु":
                return self.parse_break_statement()
            elif keyword == "अनुवर्तते":
                return self.parse_continue_statement()
        elif token and token[0] == "IDENTIFIER":
            # Determine if the identifier is part of a function call or an assignment
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            statement = None
            if next_token and next_token[1] == "(":
                statement = self.parse_function_call()  # Parse function call
                self.consume("PUNCTUATION")  # Consume the semicolon
                return statement
            else:
                statement = self.parse_assignment_expression()  # Parse assignment
                self.consume("PUNCTUATION")  # Consume the semicolon
                return statement

        raise SyntaxError(f"Unexpected token '{token[1]}' in statement, at line {token[2]} column {token[3]} ")
    
    def parse_code_block(self): 
        # Parse a block of code enclosed in curly braces
        body = []

        self.consume("PUNCTUATION")  # Consume the opening curly brace "{"
        while self.current() and self.current()[1] != "}":
            statement = self.parse_statement()
            if statement:
                body.append(statement)
        self.consume("PUNCTUATION")  # Consume the closing curly brace "}"
        
        return {
            "type": "BlockStatement",
            "body": body
        }

    def parse_main_function(self):
        # Parse the main function block

        self.consume("KEYWORD")  # Consume "मुख्यः"
        self.consume("PUNCTUATION")  # Consume "("
        self.consume("PUNCTUATION")  # Consume ")"

        body = self.parse_code_block()
        
        return {
            "type": "MainFunction",
            "id":  {
                "type": "IdentifierExpression",
                "name": "मुख्यः"
            },
            "parameters": [],
            "body": body
        }

    def parse_function_defination(self):
        # Parse a function definition
        self.consume("KEYWORD")  # Consume "कार्य"
        identifier_token = self.consume("IDENTIFIER")[1]

        self.consume("PUNCTUATION")  # Consume "("
        parameters = None
        if self.current() and self.current()[1] != ")":
            parameters = self.parse_expression_list()
        self.consume("PUNCTUATION")  # Consume ")"

        body = self.parse_code_block()

        return {
            "type": "FunctionDefination",
            "id":  {
                "type": "IdentifierExpression",
                "name": identifier_token
            },
            "parameters": parameters,
            "body": body
        }

    def parse_function_call(self):
        # Parse a function call expression
        identifier_token = self.consume("IDENTIFIER")[1]
        self.consume("PUNCTUATION")  # Consume "("

        arguments = []
        if self.current() and self.current()[1] != ")":
            arguments = self.parse_expression_list()

        self.consume("PUNCTUATION")  # Consume ")"
        return {
            "type": "FunctionCall",
            "callee": {
                "type": "IdentifierExpression",
                "name": identifier_token
            },
            "arguments": arguments
        }

    def parse_return_statement(self):
        # Parse a return statement
        self.consume("KEYWORD")  # Consume "प्रतिददाति"
        expression = self.parse_expression()
        self.consume("PUNCTUATION")  # Consume the semicolon
        return {"type": "ReturnStatement", "argument": expression}

    def parse_variable_declaration(self):
        # Parse a variable declaration
        self.consume("KEYWORD")  # Consume "चरः"

        identifier_token = self.consume("IDENTIFIER")[1]  # Parse the identifier

        self.consume("ASSIGNMENT_OPERATOR")  # Consume the "=" operator

        initializer_token = self.parse_expression()  # Parse the initializer expression

        self.consume("PUNCTUATION")  # Consume the semicolon

        return {
            "type": "VariableDeclaration",
            "id":  {
                "type": "IdentifierExpression",
                "name": identifier_token
            },
            "init": initializer_token
        }
        
    def parse_if_statement(self):
        # Consume the "यदि" keyword for "if"
        self.consume("KEYWORD")  # Consume "यदि"

        # Consume the opening parenthesis "("
        self.consume("PUNCTUATION")  # Consume "("

        # Parse the test condition (expression)
        test = self.parse_expression()

        # Consume the closing parenthesis ")"
        self.consume("PUNCTUATION")  # Consume ")"

        body = self.parse_code_block()

        # Now handle the else-if and else clauses
        alternates = []
        while self.current() and self.current()[1] == "अन्यथा यदि":  # "else if" case
            alternates.append(self.parse_else_if_statement())

        if self.current() and self.current()[1] == "अन्यथा":  # "else" case
            alternates.append(self.parse_else_statement())

        # Return the AST node for the if statement
        return {
            "type": "IfStatement",
            "test": test,
            "body" : body,
            "alternates": alternates
        }

    def parse_else_if_statement(self):
        # Consume the "अन्यथा यदि" keyword for "else if"
        self.consume("KEYWORD")  # Consume "अन्यथा यदि"

        # Consume the opening parenthesis "("
        self.consume("PUNCTUATION")  # Consume "("

        # Parse the test condition (expression)
        test = self.parse_expression()

        # Consume the closing parenthesis ")"
        self.consume("PUNCTUATION")  # Consume ")"

        body = self.parse_code_block()

        # Return the AST node for the else if statement
        return {
            "type": "IfStatement",
            "test": test,
            "body" : body,
            "alternates": []
        }
        
    def parse_else_statement(self):
        # Consume the "अन्यथा" keyword for "else"
        self.consume("KEYWORD")  # Consume "अन्यथा"

        body = self.parse_code_block()

        # Return the AST node for the else statement
        return {
            "type": "ElseStatement",
            "body": body
        }

    def parse_while_statement(self):
        # Consume the "यावद्‌" keyword
        self.consume("KEYWORD")
    
        # Consume the opening parenthesis "("
        self.consume("PUNCTUATION")
    
        # Parse the test expression (e.g., the condition inside the while loop)
        test_expression = self.parse_expression()
    
        # Consume the closing parenthesis ")"
        self.consume("PUNCTUATION")
    
        body = self.parse_code_block()
    
        # Return the structured JSON for the while statement
        return {
            "type": "WhileStatement",
            "test": test_expression,
            "body": body
        }


    def parse_break_statement(self):
        self.consume("KEYWORD")  # Expect "विरमतु"
        self.consume("PUNCTUATION")  # Expect ";"
        return {"type": "BreakStatement"}

    def parse_continue_statement(self):
        self.consume("KEYWORD")  # Expect "अनुवर्तते"
        self.consume("PUNCTUATION")  # Expect ";"
        return {"type": "ContinueStatement"}

    def parse_print_statement(self):
        # Consume the "मुद्रणम्" keyword
        self.consume("KEYWORD")  # Consume "मुद्रणम्"

        # Consume the opening parenthesis "("
        self.consume("PUNCTUATION")  # Consume "("

        # Parse the arguments
        arguments = None
        if self.current() and self.current()[1] != ")":
            arguments = self.parse_expression_list()

        # Consume the closing parenthesis ")"
        self.consume("PUNCTUATION")  # Consume ")"

        # Consume the semicolon ";"
        self.consume("PUNCTUATION")  # Consume ";"

        # Return the AST node
        return {
            "type": "PrintStatement",
            "arguments": arguments
        }
        
    def parse_expression_list(self):
        expressions = [self.parse_expression()]  # Parse the first expression

        # Parse additional expressions separated by commas
        while self.current() and self.current()[1] == ",":
            self.consume("PUNCTUATION")  # Consume ","
            expressions.append(self.parse_expression())

        return expressions
    
    def parse_expression(self):
        # Parse the left-hand side expression
        left = self.parse_primary_expression()

        # Check if the next token is a logical operator
        while self.current() and (self.current()[0] == "BINARY_OPERATOR" or self.current()[0] == "LOGICAL_OPERATOR"):
            if self.current()[0] == "LOGICAL_OPERATOR":
                operator = self.consume("LOGICAL_OPERATOR")[1]  # Consume the logical operator
                right = self.parse_expression()  # Parse the right-hand side expression

                # Construct a LogicalExpression node
                left = {
                    "type": "LogicalExpression",
                    "operator": operator,
                    "left": left,
                    "right": right
                }
            elif self.current()[0] == "BINARY_OPERATOR":
                operator = self.consume("BINARY_OPERATOR")[1]  # Consume the binary operator
                right = self.parse_primary_expression()  # Parse the right-hand side expression

                # Construct a BinaryExpression node
                left = {
                    "type": "BinaryExpression",
                    "operator": operator,
                    "left": left,
                    "right": right
                }

        return left


    def parse_primary_expression(self):
        token = self.current()

        if token[0] == "IDENTIFIER":
            # Check if the next token is a parenthesis indicating a function call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][1] == "(":
                return self.parse_function_call()  # Parse as a function call
            # Otherwise, treat it as an identifier expression
            return {
                "type": "IdentifierExpression",
                "name": self.consume("IDENTIFIER")[1]
            }
        elif token[0] == "NUMBER":
            # Consume the number
            return {
                "type": "NumericLiteral",
                "value": int(self.consume("NUMBER")[1])
            }
        elif token[0] == "FLOAT":
            # Consume the float
            return {
                "type": "FloatLiteral",
                "value": float(self.consume("FLOAT")[1])
            }
        elif token[0] == "STRING":
            # Consume the string
            return {
                "type": "StringLiteral",
                "value": self.consume("STRING")[1]
            }
        elif token[0] == "BOOLEAN":
            # Consume the boolean
            return {
                "type": "BooleanLiteral",
                "value": self.consume("BOOLEAN")[1] == "सत्य"
            }
        elif token[0] == "NULL":
            #consume null
            self.consume("NULL")
            return{
                "type": "Null",
                "value": None
            }
        elif token[1] == "(":
            # Handle parenthesized expressions
            self.consume("PUNCTUATION")  # Consume "("
            expression = self.parse_expression()
            self.consume("PUNCTUATION")  # Consume ")"
            return expression
        else:
            raise SyntaxError(f"Unexpected token: '{token[1]}', at line {token[2]} column {token[3]}")

    def parse_assignment_expression(self):
        # Parse the left-hand side expression (which could be an identifier)
        left = self.parse_primary_expression()

        # Check if the next token is an assignment operator (e.g., '=', '+=', '-=')
        if self.current() and self.current()[0] == "ASSIGNMENT_OPERATOR":
            operator = self.consume("ASSIGNMENT_OPERATOR")[1]  # Consume the assignment operator
            right = self.parse_expression()  # Parse the right-hand side expression

            # Construct the assignment expression node
            return {
                "type": "AssignmentExpression",
                "operator": operator,
                "left": left,
                "right": right
            }   

        # If no assignment operator, return the left expression (could be a simple variable or value)
        return left