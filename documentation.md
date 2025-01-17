# VedaSkript : Sanskrit-based Toy Programming Language

This toy programming language is based on Sanskrit keywords and operators. The language includes features like variables, basic operations, loops, conditions, and built-in functions, all expressed in Sanskrit.

---

## Keywords

- **कार्य मुख्यः**: main function
- **कार्य**: function defination
- **चरः**: Declares a variable
- **मुद्रणम्**: Built-in function for printing
- **यदि**: If condition
- **अन्यथा यदि**: Else if
- **अन्यथा**: Else
- **यावद्‌**: While loop
- **अनुवर्तते**: Continue to the next iteration
- **विरमतु**: Break out of the loop
- **रिक्त**: Null
- **सत्य**: True
- **असत्य**: False
- **प्रतिददाति**: Return

---

## Operators

### Binary:

- `+`, `-`, `*`, `/`, `%`, `==`, `>=`, `<=`, `<`, `>`, `!=`

### Logical:

- `||`, `&&`

### Assignment:

- `=`, `-=`, `+=`, `*=`, `/=`, `%=`

## Comments

### Single line comments

- `//single line comments will be placed here`

### Multi line comments

- `/*multi line comments will be placed here*/`

---

## AST

### Blank Programme

#### AST

```json
{
  "type": "SanskritProgram",
  "body": []
}
```

---

### Main Function

- #### Programme

```
कार्य मुख्यः(){
    //code here
}
```

- #### AST

```json
{
  "type": "mainFunction",
  "id": {
    "type": "IdentifierExpression",
    "name": "मुख्यः"
  },
  "parameters": [],
  "body": {
    "type": "BlockStatement",
    "body": []
  }
}
```

---

### Function Defination

- #### Programme

```
कार्य  योग(/*parameters here seperated by ,*/){
    //code here
}
```

- #### AST

```json
{
  "type": "FunctionDefination",
  "id": {
    "type": "IdentifierExpression",
    "name": " योग"
  },
  "parameters": null,
  "body": {
    "type": "BlockStatement",
    "body": []
  }
}
```

---

### Code Block

- #### Programme

```
{
    //code here
}
```

- #### AST

```json
{
  "type": "BlockStatement",
  "body": []
}
```

---

### Identifier Expression

- #### Programme

```
संख्या
```

- #### AST

```json
{
  "type": "IdentifierExpression",
  "name": "संख्या"
}
```

---

### Numerical Literal

- #### Programme

```
10
```

- #### AST

```json
{
  "type": "NumericLiteral",
  "value": 10
}
```

---

### Float Literal

- #### Programme

```
10.1
```

- #### AST

```json
{
  "type": "FloatLiteral",
  "value": 10.1
}
```

---

### String Literal

- #### Programme

```
"छोटी"
```

- #### AST

```json
{
  "type": "StringLiteral",
  "value": "\"छोटी\""
}
```

---

### Bollean Literal

- #### Programme

```
सत्य
```

- #### AST

```json
{
  "type": "BooleanLiteral",
  "value": True
}
```

---

### Null Value

- #### Programme

```
रिक्त
```

- #### AST

```json
{
  "type": "Null",
  "value": null
}
```

---

### Variable Declaration

- #### Programme

```
चरः संख्या = 10;
```

- #### AST

```json
{
  "type": "VariableDeclaration",
  "id": {
    "type": "IdentifierExpression",
    "name": "संख्या"
  },
  "init": {
    "type": "NumericLiteral",
    "value": 10
  }
}
```

---

### Assignment Operator

- #### Programme

```
संख्या = 10;
```

- #### AST

```json
{
  "type": "AssignmentExpression",
  "operator": "=",
  "left": {
    "type": "IdentifierExpression",
    "name": "संख्या"
  },
  "right": {
    "type": "NumericLiteral",
    "value": 10
  }
}
```

---

### Binary Operator

- #### Programme

```
5 < 10
```

- #### AST

```json
{
  "type": "BinaryExpression",
  "operator": "<",
  "left": {
    "type": "NumericLiteral",
    "value": 5
  },
  "right": {
    "type": "NumericLiteral",
    "value": 10
  }
}
```

---

### Logical Operator

- #### Programme

```
असत्य || सत्य
```

- #### AST

```json
{
  "type": "LogicalExpression",
  "operator": "||",
  "left":
  {
    "type": "BooleanLiteral",
    "value": False
  },
  "right":
  {
    "type": "BooleanLiteral",
    "value": True
  }
}
```

---

### If Else Statement

- #### Programme

```
यदि (/*condition here*/) {
  //code here
}
अन्यथा यदि (/*condition here*/) {
  //code here
}
अन्यथा यदि (/*condition here*/) {
  //code here
}अन्यथा {
  //code here
}
```

- #### AST

```json
{
  "type": "IfStatement",
  "test": {},
  "body": { "type": "BlockStatement", "body": [] },
  "alternates": [
    {
      "type": "IfStatement",
      "test": {},
      "body": { "type": "BlockStatement", "body": [] },
      "alternates": []
    },
    {
      "type": "IfStatement",
      "test": {},
      "body": { "type": "BlockStatement", "body": [] },
      "alternates": []
    },
    {
      "type": "ElseStatement",
      "body": { "type": "BlockStatement", "body": [] }
    }
  ]
}
```

---

### While Loop

- #### Programme

```
यावद्‌ (/*condition here*/) {
  //code here
}
```

- #### AST

```json
{
  "type": "WhileStatement",
  "test": {},
  "body": { "type": "BlockStatement", "body": [] }
}
```

---

### Function Call

- #### Programme

```
चोदुः(/*arguments here seperated by ,*/);
```

- #### AST

```json
{
  "type": "FunctionCall",
  "callee": {
    "type": "IdentifierExpression",
    "name": "चोदुः"
  },
  "arguments": []
}
```

---

### Print Statement

- #### Programme

```
मुद्रणम्(/*arguments here seperated by ,*/);
```

- #### AST

```json
{
  "type": "PrintStatement",
  "arguments": []
}
```

---

### Break Statement

- #### Programme

```
विरमतु;
```

- #### AST

```json
{ "type": "BreakStatement" },
```

---

### Continue Statement

- #### Programme

```
अनुवर्तते;
```

- #### AST

```json
{ "type": "ContinueStatement" },
```

---

### Return Statement

- #### Programme

```
प्रतिददाति a ;
```

- #### AST

```json
{
  "type": "ReturnStatement",
  "argument": { "type": "IdentifierExpression", "name": "a" }
}
```

---
