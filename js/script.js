let pyodide; // Global variable for Pyodide
let executorLoaded = false; // Flag to track if executor.py is loaded

vedaskriptFiles = [
  "https://vedaskript.vercel.app/modules/executor.py",
  "https://vedaskript.vercel.app/modules/parser.py",
  "https://vedaskript.vercel.app/modules/tokenizer.py",
  "https://vedaskript.vercel.app/modules/validator.py",
  "https://vedaskript.vercel.app/modules/codegenerator.py",
];

// Function to initialize Pyodide and load all required files
async function initializePyodide() {
  if (!pyodide) {
    // Load Pyodide once
    pyodide = await loadPyodide();
    console.log("Pyodide loaded");
  }

  if (!executorLoaded) {
    // Load all required files once
    for (const fileUrl of vedaskriptFiles) {
      const response = await fetch(fileUrl);
      const scriptContent = await response.text();
      const fileName = fileUrl.split("/").pop();
      pyodide.FS.writeFile(fileName, scriptContent);
      console.log(`${fileName} loaded`);
    }
    executorLoaded = true;
  }
}

async function executeCode() {
  const outputElement = document.getElementById("output");
  const sanskritCode = window.editor.getValue();

  outputElement.textContent = "Executing code...";

  try {
    // Ensure Pyodide and executor.py are initialized
    await initializePyodide();

    // Run Sanskrit code
    const resultJson = pyodide.runPython(`
from executor import process_sanskrit_code
process_sanskrit_code(${JSON.stringify(sanskritCode)})
          `);

    // Parse the JSON response
    const result = JSON.parse(resultJson);

    // Check for errors
    if (result.error) {
      outputElement.textContent = `Error: ${result.error}`;
      outputElement.style = "color: red;";
    } else {
      // Display the output details
      outputElement.textContent = "Compilation and Execution Results:\n\n";
      outputElement.style = "color: white;";

      for (const step of result.output) {
        if (step.type == "ProgrammeOutput") {
          outputElement.textContent += `${step.output}`;
        }
      }
    }
  } catch (error) {
    outputElement.textContent = `Error: ${error.message}`;
    console.error(error);
  }
}

async function clearEditor(params) {
  window.editor.setValue("");
}

async function saveCode() {
  const code = window.editor.getValue();
  const blob = new Blob([code], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "vedaskript.vds";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function copyCode(button) {
  // Find the code block inside the same container
  const codeBlock = button.closest(".code-container").querySelector("code");

  // Extract the text content and trim whitespace
  const codeText = codeBlock.textContent.trim();

  // Copy to clipboard
  navigator.clipboard.writeText(codeText).then(
    () => {
      button.style = "background-color: transparent";
      const icon = button.querySelector("i");
      if (icon) {
        icon.style.color = "white";
      }
    },
    (err) => {
      button.style = "background-color: #ffffff";
      const icon = button.querySelector("i");
      if (icon) {
        icon.style.color = "#1e1e1e";
      }
    }
  );
}

let darkTheme = false;

function changeTheme() {
  if (darkTheme) {
    document.body.style.backgroundColor = "white";
    document.body.style.color = "#182e6a";
    darkTheme = false;
  } else {
    document.body.style.backgroundColor = "#121212";
    document.body.style.color = "white";
    darkTheme = true;
  }
}
