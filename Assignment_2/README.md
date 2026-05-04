# Config File Parser – VS Code Extension

A Visual Studio Code extension that provides a Webview-based tool to upload and parse JSON configuration files. The extension validates the uploaded file, parses its contents, and displays appropriate success or error messages to the user within the Webview.

---

## Features

- Upload a single configuration file
- Supports only JSON (`.json`) files
- Enforces a maximum file size limit of 20MB
- Uses JavaScript FileReader to read file content
- Secure communication between Webview and extension backend
- Parses uploaded JSON on the backend
- Displays success and failure messages in the Webview

---

## Technologies Used

- JavaScript
- Visual Studio Code Extension API
- HTML
- CSS
- Webview API
- FileReader API

---

## Project Structure

- extension.js – Main extension backend logic
- package.json – Extension metadata and command registration
- README.md – Project documentation
- jsconfig.json – JavaScript type checking configuration
- .vscode folder – Debug and launch settings

---

## Installation

- Clone the repository
- Open the project folder in Visual Studio Code
- Install dependencies using npm if required

---

## Running the Extension

- Press F5 to launch the Extension Development Host
- Open the Command Palette using Ctrl + Shift + P
- Run the command Open Config File Parser
- The Webview interface will open

---

## How It Works

- The Webview provides a file upload interface for JSON files
- File type and size are validated on the client side
- JavaScript FileReader reads the file contents as text
- The content is sent to the extension backend using vscode.postMessage
- The backend parses the JSON file
- A success or error message is sent back to the Webview

---

## Error Handling

- Uploading non-JSON files displays an error
- Files larger than 20MB are rejected
- Invalid or malformed JSON results in an error message

---

## Example JSON File

```json
{
  "appName": "SampleApp",
  "version": 1,
  "environment": "development"
}
```

## Assignment Coverage

- Webview creation  
- Single file upload support  
- FileReader usage  
- File type and size validation  
- Backend JSON parsing  
- User feedback through success and failure messages  

---
