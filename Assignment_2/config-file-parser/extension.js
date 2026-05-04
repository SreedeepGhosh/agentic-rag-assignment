const vscode = require('vscode');


/**
 * @param {import('vscode').ExtensionContext} context
 */


function activate(context) {

    const disposable = vscode.commands.registerCommand(
        'configParser.openWebview',
        function () {

            const panel = vscode.window.createWebviewPanel(
                'configParser',
                'Config File Parser',
                vscode.ViewColumn.One,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent();

            panel.webview.onDidReceiveMessage((message) => {
                if (message.command === 'upload') {
                    try {
                        const parsedJson = JSON.parse(message.text);
                        console.log(parsedJson);

                        panel.webview.postMessage({
                            status: 'success',
                            message: 'File processed successfully!'
                        });
                    } catch {
                        panel.webview.postMessage({
                            status: 'error',
                            message: 'Invalid JSON file!'
                        });
                    }
                }
            });
        }
    );

    context.subscriptions.push(disposable);
}

function getWebviewContent() {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Config File Parser</title>
        <style>
            body { font-family: Arial; padding: 25px; }
            #error { color: red; }
            #success { color: green; }
        </style>
    </head>
    <body>

    <h2>Upload Configuration File (.json)</h2>

    <input type="file" id="fileInput" accept=".json" />
    <p id="error"></p>
    <p id="success"></p>

    <script>
        const vscode = acquireVsCodeApi();
        const fileInput = document.getElementById('fileInput');
        const errorEl = document.getElementById('error');
        const successEl = document.getElementById('success');

        fileInput.addEventListener('change', () => {
            errorEl.textContent = '';
            successEl.textContent = '';

            const file = fileInput.files[0];
            if (!file) return;

            if (!file.name.endsWith('.json')) {
                errorEl.textContent = 'Only JSON files are allowed.';
                return;
            }

            if (file.size > 20 * 1024 * 1024) {
                errorEl.textContent = 'File size exceeds 20MB.';
                return;
            }

            const reader = new FileReader();
            reader.onload = () => {
                vscode.postMessage({
                    command: 'upload',
                    text: reader.result
                });
            };
            reader.readAsText(file);
        });

        window.addEventListener('message', event => {
            if (event.data.status === 'success') {
                successEl.textContent = event.data.message;
            } else if (event.data.status === 'error') {
                errorEl.textContent = event.data.message;
            }
        });
    </script>

    </body>
    </html>`;
}

function deactivate() {}

module.exports = { activate, deactivate };