class ASTValidator:
    def __init__(self,ast, debug=False):
        self.ast = ast
        self.debug = debug
        self.errors = []
        self.global_variables = set()
        self.function_definitions = set()
        self.current_function_scope = None
        self.local_variables = {}

    def validate(self):
        """Entry point for validating the AST."""
        self.errors.clear()
        self.global_variables.clear()
        self.function_definitions.clear()
        self.local_variables.clear()
        self.current_function_scope = None

        self._collect_definitions(self.ast)
        
        self._validate_node(self.ast)
        return {"type" : "ValidatorOutput", "response": not self.errors, "errors": self.errors}
    
    def _collect_definitions(self, node):
        """Collect all function definitions and global variables."""
        if node["type"] == "SanskritProgram":
            if "body" not in node or not isinstance(node["body"], list):
                self.errors.append("SanskritProgram must have a 'body' of type list.")
            for child in node.get("body", []):
                self._collect_definitions(child)
        elif node["type"] == "FunctionDefination" or node["type"] == "MainFunction":
            function_name = node["id"]["name"]
            if function_name in self.function_definitions:
                self.errors.append(f"Function '{function_name}' is already defined.")
            else:
                self.function_definitions.add(function_name)
        elif node["type"] == "VariableDeclaration":
            variable_name = node["id"]["name"]
            if self.current_function_scope is None:
                # Global variable
                if variable_name in self.global_variables:
                    self.errors.append(f"Global variable '{variable_name}' is already defined.")
                self.global_variables.add(variable_name)
        else:
            self.errors.append(f"Unknown node type outside main: {node['type']}")

    def _validate_node(self, node):
        """Recursive validation of an AST node."""
        node_type = node.get("type")
        if self.debug:
            print(f"Validating node: {node_type}")

        if node_type == "SanskritProgram":
            self._validate_program(node)
        elif node_type == "MainFunction":
            self._validate_main_function(node)
        elif node_type == "FunctionDefination":
            self._validate_function_definition(node)
        elif node_type == "BlockStatement":
            self._validate_block_statement(node)
        elif node_type == "VariableDeclaration":
            self._validate_variable_declaration(node)
        elif node_type == "AssignmentExpression":
            self._validate_assignment_expression(node)
        elif node_type == "BinaryExpression":
            self._validate_binary_expression(node)
        elif node_type == "LogicalExpression":
            self._validate_logical_expression(node)
        elif node_type == "IfStatement":
            self._validate_if_statement(node)
        elif node_type == "ElseStatement":
            self._else_statement(node)
        elif node_type == "WhileStatement":
            self._validate_while_statement(node)
        elif node_type == "FunctionCall":
            self._validate_function_call(node)
        elif node_type == "PrintStatement":
            self._validate_print_statement(node)
        elif node_type in {"BreakStatement", "ContinueStatement", "ReturnStatement"}:
            self._validate_simple_statement(node)
        else:
            self.errors.append(f"Unknown node type: {node_type}")

    def _validate_program(self, node):
        if "body" not in node or not isinstance(node["body"], list):
            self.errors.append("SanskritProgram must have a 'body' of type list.")
        for child in node.get("body", []):
            if child["type"] == "FunctionDefination" or child["type"] == "MainFunction":
                self._validate_node(child)

    def _validate_main_function(self, node):
        if "id" not in node or node["id"].get("name") != "मुख्यः":
            self.errors.append("mainFunction must have an id with the name 'मुख्यः'.")
        self.current_function_scope = "मुख्यः"
        self.local_variables[self.current_function_scope] = set()
        
        for param in node.get("parameters", []):
            if param["type"] != "IdentifierExpression":
                self.errors.append("Function parameter must have a name.")
            if "name" not in param:
                self.errors.append("Function parameter must have a name.")
            param_name = param["name"]
            if param_name in self.global_variables:
                self.errors.append(f"Parameter '{param_name}' is already defined as globle variable'.")
            self.local_variables[function_name].add(param_name)
        
        self._validate_node(node.get("body", {}))
        self.current_function_scope = None

    def _validate_function_definition(self, node):
        if "id" not in node or "name" not in node["id"]:
            self.errors.append("FunctionDefination must have a valid id.")
        if "body" not in node:
            self.errors.append("FunctionDefination must have a body.")
        function_name = node["id"]["name"]
        self.current_function_scope = function_name
        self.local_variables[function_name] = set()
        
        for param in node.get("parameters", []):
            if param["type"] != "IdentifierExpression":
                self.errors.append("Function parameter must have a name.")
            if "name" not in param:
                self.errors.append("Function parameter must have a name.")
            param_name = param["name"]
            if param_name in self.global_variables:
                self.errors.append(f"Parameter '{param_name}' is already defined as globle variable.")
            self.local_variables[function_name].add(param_name)
        
        self._validate_node(node.get("body", {}))
        self.current_function_scope = None
        
    def _validate_block_statement(self, node):
        if "body" not in node or not isinstance(node["body"], list):
            self.errors.append("BlockStatement must have a 'body' of type list.")
        for child in node.get("body", []):
            self._validate_node(child)

    def _validate_variable_declaration(self, node):
        if "id" not in node or "name" not in node["id"]:
            self.errors.append("VariableDeclaration must have a valid id.")
        if "init" not in node:
            self.errors.append("VariableDeclaration must have an initializer.")

        variable_name = node["id"]["name"]
        if self.current_function_scope:
            if variable_name in self.local_variables[self.current_function_scope]:
                self.errors.append(f"Variable '{variable_name}' is already defined in function '{self.current_function_scope}'.")
            self.local_variables[self.current_function_scope].add(variable_name)
        else:
            if variable_name in self.global_variables:
                self.errors.append(f"Global variable '{variable_name}' is already defined.")
            self.global_variables.add(variable_name)

    def _validate_assignment_expression(self, node):
        if "operator" not in node or node["operator"] not in {"=", "+=", "-=", "*=", "/=", "%="}:
            self.errors.append("Invalid operator in AssignmentExpression.")
        if "left" not in node or "right" not in node:
            self.errors.append("AssignmentExpression must have 'left' and 'right'.")
            
        variable_name = node["left"]["name"]
        if self.current_function_scope:
            if variable_name not in self.local_variables[self.current_function_scope]:
                self.errors.append(f"Variable '{variable_name}' is not defined in function '{self.current_function_scope}'.")
        elif variable_name not in self.global_variables:
            self.errors.append(f"Global variable '{variable_name}' is not defined.")

    def _validate_binary_expression(self, node):
        if "operator" not in node or node["operator"] not in {"+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="}:
            self.errors.append("Invalid operator in BinaryExpression.")
        if "left" not in node or "right" not in node:
            self.errors.append("BinaryExpression must have 'left' and 'right'.")

    def _validate_logical_expression(self, node):
        if "operator" not in node or node["operator"] not in {"||", "&&"}:
            self.errors.append("Invalid operator in LogicalExpression.")
        if "left" not in node or "right" not in node:
            self.errors.append("LogicalExpression must have 'left' and 'right'.")

    def _validate_if_statement(self, node):
        if "test" not in node or "body" not in node:
            self.errors.append("IfStatement must have 'test' and 'body'.")
        self._validate_node(node.get("body", {}))
        for alternate in node.get("alternates", []):
            self._validate_node(alternate)
            
    def _else_statement(self, node):
        if "body" not in node:
            self.errors.append("ElseStatement must have a 'body'.")
        self._validate_node(node.get("body", {}))

    def _validate_while_statement(self, node):
        if "test" not in node or "body" not in node:
            self.errors.append("WhileStatement must have 'test' and 'body'.")
        self._validate_node(node.get("body", {}))

    def _validate_function_call(self, node):
        if "callee" not in node or "name" not in node["callee"]:
            self.errors.append("FunctionCall must have a valid callee.")
        if "arguments" not in node or not isinstance(node["arguments"], list):
            self.errors.append("FunctionCall must have arguments of type list.")
            
        function_name = node["callee"]["name"]
        if function_name not in self.function_definitions:
            self.errors.append(f"Function '{function_name}' is not defined.")

    def _validate_print_statement(self, node):
        if "arguments" not in node or not isinstance(node["arguments"], list):
            self.errors.append("PrintStatement must have arguments of type list.")

    def _validate_simple_statement(self, node):
        if "type" not in node:
            self.errors.append(f"Invalid simple statement: {node}")