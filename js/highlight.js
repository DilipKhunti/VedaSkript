Prism.languages.vedaskript = {
  comment: {
    pattern: /\/\/[^\n]*|\/\*.*?\*\//gmu,
    greedy: true,
  },
  keyword: {
    pattern:
      /कार्य मुख्यः|चरः|मुद्रणम्|यदि|अन्यथा यदि|अन्यथा|यावद्‌|अनुवर्तते|विरमतु|कार्य|प्रतिददाति/gmu,
    greedy: true,
  },
  "logical-operator": {
    pattern: /&&|\|\|/gmu,
    alias: "operator",
  },
  "comparison-operator": {
    pattern: /==|<=|>=|<|>|!=/gmu,
    alias: "operator",
  },
  "assignment-operator": {
    pattern: /=|\+=|-=|\*=|\/=|%=/gmu,
  },
  "arithmetic-operator": {
    pattern: /\+|-|\*|\/|%/gmu,
    alias: "operator",
  },
  boolean: {
    pattern: /सत्य|असत्य/gmu,
    alias: "boolean",
  },
  null: {
    pattern: /रिक्त/gmu,
    alias: "null",
  },
  identifier: {
    pattern: /[अ-हa-zA-Z\u0900-\u097F]+(?:[अ-हa-zA-Z0-9_])*/gmu,
    alias: "variable",
  },
  number: {
    pattern: /\b[0-9]+\b/gmu,
    alias: "number",
  },
  float: {
    pattern: /\b[0-9]+\.[0-9]+\b/gmu,
    alias: "number",
  },
  string: {
    pattern: /"(\\.|[^\\"])*"/gmu,
    greedy: true,
  },
  punctuation: {
    pattern: /[{}();,]/gmu,
    alias: "punctuation",
  },
  whitespace: {
    pattern: /\s+/gmu,
    alias: "whitespace",
  },
};

Prism.highlightAll();
