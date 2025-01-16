import io
import sys
import json

import tokenizer as tkn
import parser as pa
import validator as val
import codegenerator as cg


# Function to execute Python code and capture its output
def capture_exec_output(python_code):
    captured_output = io.StringIO()
    original_stdout = sys.stdout

    try:
        sys.stdout = captured_output  # Redirect output
        exec(python_code, {})  # Use an isolated environment
    except Exception as e:
        captured_output.write(f"Error: {e}")
    finally:
        sys.stdout = original_stdout  # Restore original stdout

    return captured_output.getvalue()


# Main function to process Sanskrit code
def process_sanskrit_code(code):
    try:
        # Tokenize
        tokenizer = tkn.Tokenizer(code, debug=False)
        tokenizer_output = tokenizer.tokenize()

        if not tokenizer_output["response"]:
            return json.dumps({"error": tokenizer_output["message"]}, ensure_ascii=False)

        # Parse
        parser = pa.Parser(tokenizer_output["tokens"], debug=False)
        parser_output = parser.parse_program()

        if not parser_output["response"]:
            return json.dumps({"error": parser_output["message"]}, ensure_ascii=False)

        # Validate
        validator = val.ASTValidator(parser_output["AST"], debug=False)
        validator_output = validator.validate()

        if not validator_output["response"]:
            return json.dumps({"error": validator_output["errors"]}, ensure_ascii=False)

        # Generate Python code
        codegen = cg.CodeGenerator(parser_output["AST"])
        python_code = codegen.generate()

        # Execute the Python code and capture the output
        programme_output = capture_exec_output(python_code)

        # Return all results as JSON
        output = {
            "type": "CompilerOutput",
            "output": [
                tokenizer_output,
                parser_output,
                validator_output,
                {"type": "PythonCode", "code": python_code},
                {"type": "ProgrammeOutput", "output": programme_output},
            ],
        }
        return json.dumps(output, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, ensure_ascii=False)
