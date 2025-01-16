class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.indent_level = 0

    def generate(self):
        code = self._generate_node(self.ast)
        # Append main() call at the end of the code
        code += "\nmain()"
        return code

    def _indent(self):
        return "    " * self.indent_level

    def _generate_block(self, statements):
        # Generate code for a block of statements with proper indentation
        self.indent_level += 1
        code = "\n".join(self._indent() + self._generate_node(stmt) for stmt in statements)
        self.indent_level -= 1
        return code

    def _generate_node(self, node):
        if node["type"] == "SanskritProgram":
            return "\n".join(self._generate_node(stmt) for stmt in node["body"])
        elif node["type"] == "VariableDeclaration":
            return f"{node['id']['name']} = {self._generate_node(node['init'])}"
        elif node["type"] == "MainFunction":
            body = self._generate_block(node["body"]["body"])
            return f"def main():\n{body}"
        elif node["type"] == "NumericLiteral":
            return str(node["value"])
        elif node["type"] == "FloatLiteral":
            return str(node["value"])
        elif node["type"] == "BooleanLiteral":
            return "True" if node["value"] else "False"
        elif node["type"] == "StringLiteral":
            return str(node["value"])
        elif node["type"] == "Null":
            return "None"
        elif node["type"] == "IdentifierExpression":
            return node["name"]
        elif node["type"] == "PrintStatement":
            args = ", ".join(self._generate_node(arg) for arg in node["arguments"])
            return f"print({args})"
        elif node["type"] == "IfStatement":
            test = self._generate_node(node["test"])
            body = self._generate_block(node["body"]["body"])
            code = f"if {test}:\n{body}"
    
            # Handle elif and else
            for alternate in node.get("alternates", []):
                if alternate["type"] == "IfStatement":
                    test = self._generate_node(alternate["test"])
                    body = self._generate_block(alternate["body"]["body"])
                    code += f"\n{self._indent()}elif {test}:\n{body}"
                elif alternate["type"] == "ElseStatement":
                    body = self._generate_block(alternate["body"]["body"])
                    code += f"\n{self._indent()}else:\n{body}"
            return code

        elif node["type"] == "BinaryExpression":
            left = self._generate_node(node["left"])
            right = self._generate_node(node["right"])
            return f"{left} {node['operator']} {right}"
        elif node["type"] == "WhileStatement":
            test = self._generate_node(node["test"])
            body = self._generate_block(node["body"]["body"])
            return f"while {test}:\n{body}"
        elif node["type"] == "AssignmentExpression":
            left = self._generate_node(node["left"])
            right = self._generate_node(node["right"])
            return f"{left} {node['operator']} {right}"
        elif node["type"] == "FunctionCall":
            callee = self._generate_node(node["callee"])
            args = ", ".join(self._generate_node(arg) for arg in node["arguments"])
            return f"{callee}({args})"
        elif node["type"] == "FunctionDefination":
            params = ", ".join(param["name"] for param in node["parameters"])
            body = self._generate_block(node["body"]["body"])
            return f"def {node['id']['name']}({params}):\n{body}"
        elif node["type"] == "ReturnStatement":
            return f"return {self._generate_node(node['argument'])}"
        elif node["type"] == "LogicalExpression":
            left = self._generate_node(node["left"])
            right = self._generate_node(node["right"])
            operator = "or" if node["operator"] == "||" else "and"
            return f"{left} {operator} {right}"
        elif node["type"] == "BreakStatement":
            return "break"
        elif node["type"] == "ContinueStatement":
            return "continue"
        else:
            raise ValueError(f"Unknown node type: {node['type']}")
