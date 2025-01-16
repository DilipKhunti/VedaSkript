require.config({
  paths: {
    vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs",
  },
});

require(["vs/editor/editor.main"], function () {
  // Define custom Sanskrit language
  monaco.languages.register({ id: "vedaskript" });

  monaco.languages.setMonarchTokensProvider("vedaskript", {
    tokenizer: {
      root: [
        [/\/\/[^\n]*|\/\*.*?\*\//, "comment"], // Comments
        [
          /कार्य मुख्यः|चरः|मुद्रणम्|यदि|अन्यथा यदि|अन्यथा|यावद्‌|अनुवर्तते|विरमतु|कार्य|प्रतिददाति/,
          "keyword",
        ], // Keywords
        [/&&|\|\|/, "logical-operator"], // Logical Operators
        [/==|<=|>=|<|>|!=/, "binary-operator"], // Comparison Operators
        [/=|\+=|-=|\*=|\/=|%=/, "assignment-operator"], // Assignment Operators
        [/\+|-|\*|\/|%/, "binary-operator"], // Arithmetic Operators
        [/\b(सत्य|असत्य)\b/, "boolean"], // Boolean Literals
        [/\bरिक्त\b/, "null"], // Null Literal
        [/[अ-हa-zA-Z\u0900-\u097F]+(?:[अ-हa-zA-Z0-9_])*/, "identifier"], // Identifiers
        [/[0-9]+\.[0-9]+/, "float"], // Floating-point numbers
        [/[0-9]+/, "number"], // Numbers
        [/\"(\\.|[^\\\"])*\"/, "string"], // Strings
        [/[{}();,]/, "delimiter"], // Punctuation
        [/\s+/, "white"], // Whitespace
      ],
    },
  });

  // Create Monaco Editor instance
  const editor = monaco.editor.create(document.getElementById("editor"), {
    value: `//press ctrl + SPACE for quick suggestions\n//press F1 to open command palette\n\nकार्य मुख्यः() {\n\tमुद्रणम्("नमस्ते विश्व!");\n}`,
    language: "vedaskript",
    theme: "vs-dark",
    automaticLayout: true,
    lineNumbers: "on",
    minimap: {
      enabled: window.innerWidth >= 550, // Disable minimap if display width is less than 550 px
    },
    wordWrap: "on", // Enables word wrapping
    quickSuggestions: {
      strings: true, // Enable suggestions inside strings
      comments: false, // Disable suggestions inside comments
      other: true, // Enable suggestions in other contexts
    },
    mouseWheelZoom: true,
    formatOnPaste: true,
    smoothScrolling: true,
    scrollbar: {
      alwaysConsumeMouseWheel: false, // Disable mouse wheel capture
    },
  });

  // Update minimap setting on window resize
  window.addEventListener("resize", function () {
    editor.updateOptions({
      minimap: {
        enabled: window.innerWidth >= 550,
      },
    });
  });

  // Make editor accessible globally
  window.editor = editor;

  monaco.languages.registerCompletionItemProvider("vedaskript", {
    provideCompletionItems: function (model, position) {
      return {
        suggestions: [
          {
            label: "कार्य मुख्यः", // Main function
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "कार्य मुख्यः() {\n\t${1:code}\n}",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "कार्य", // Function definition
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText:
              "कार्य ${1:functionName}(${2:parameters}) {\n\t${3:code}\n}",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "चरः", // Variable declaration
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "चरः ${1:variableName} = ${2:value};",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "यदि", // If statement
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "यदि (${1:condition}) {\n\t${2:code}\n}",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "अन्यथा यदि", // Else if statement
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "अन्यथा यदि (${1:condition}) {\n\t${2:code}\n}",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "अन्यथा", // Else statement
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "अन्यथा {\n\t${1:code}\n}",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "यावद्‌", // While loop
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "यावद्‌ (${1:condition}) {\n\t${2:code}\n}",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "मुद्रणम्", // Print statement
            kind: monaco.languages.CompletionItemKind.Function,
            insertText: "मुद्रणम्(${1:message});",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "विरमतु", // Break statement
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "विरमतु;",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "अनुवर्तते", // Continue statement
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "अनुवर्तते;",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "प्रतिददाति", // Return statement
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "प्रतिददाति ${1:value};",
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          },
          {
            label: "रिक्त", // Null value
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "रिक्त",
          },
          {
            label: "सत्य", // True boolean
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "सत्य",
          },
          {
            label: "असत्य", // False boolean
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: "असत्य",
          },
        ],
      };
    },
  });
});
