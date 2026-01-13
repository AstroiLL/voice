from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store current text in memory
current_text = ""

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Receiver</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #1a1a2e;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 700px;
            background: #16213e;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 {
            color: #e94560;
            font-size: 1.5rem;
            margin-bottom: 16px;
        }
        .status {
            color: #0f3460;
            font-size: 0.9rem;
            margin-bottom: 16px;
        }
        .status.received {
            color: #4ade80;
        }
        textarea {
            width: 100%;
            min-height: 200px;
            background: #0f3460;
            color: #e2e8f0;
            border: 2px solid #1a1a2e;
            border-radius: 8px;
            padding: 16px;
            font-size: 1rem;
            resize: vertical;
            outline: none;
        }
        textarea:focus {
            border-color: #e94560;
        }
        .buttons {
            display: flex;
            gap: 12px;
            margin-top: 16px;
        }
        button {
            padding: 12px 24px;
            font-size: 0.95rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .copy-btn {
            background: #e94560;
            color: white;
            flex: 1;
        }
        .copy-btn:hover {
            background: #ff6b6b;
        }
        .copy-btn.copied {
            background: #4ade80;
        }
        .clear-btn {
            background: #0f3460;
            color: #e2e8f0;
        }
        .clear-btn:hover {
            background: #1a1a2e;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Receiver</h1>
        <div class="status" id="status">Server running - waiting for text...</div>
        <textarea id="textArea" placeholder="Received text will appear here..."></textarea>
        <div class="buttons">
            <button class="copy-btn" onclick="copyToClipboard()">Copy to Clipboard</button>
            <button class="clear-btn" onclick="clearText()">Clear</button>
        </div>
    </div>

    <script>
        const textArea = document.getElementById('textArea');
        const status = document.getElementById('status');

        function copyToClipboard() {
            textArea.select();
            navigator.clipboard.writeText(textArea.value).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.textContent = 'Copied!';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = 'Copy to Clipboard';
                    btn.classList.remove('copied');
                }, 2000);
            });
        }

        function clearText() {
            textArea.value = '';
            status.textContent = 'Cleared';
            status.classList.remove('received');
        }

        // Poll for new text every 500ms
        async function checkForText() {
            try {
                const response = await fetch('/text');
                const data = await response.json();
                if (data.text && data.text !== textArea.value) {
                    textArea.value = data.text;
                    status.textContent = `Text received (${data.text.length} chars)`;
                    status.classList.add('received');
                }
            } catch (e) {}
            setTimeout(checkForText, 500);
        }

        checkForText();
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/text', methods=['POST'])
def receive_text():
    """Endpoint to receive text via HTTP POST"""
    global current_text

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    mode = data.get('mode', 'set')  # 'set' to replace, 'append' to add

    if mode == 'set':
        current_text = text
    else:
        current_text += text

    return jsonify({'status': 'success', 'length': len(text)}), 200


@app.route('/text', methods=['GET'])
def get_text():
    """Endpoint to get current text via HTTP GET"""
    return jsonify({'text': current_text}), 200


def main():
    from waitress import serve
    print("Server running on http://localhost:5000")
    serve(app, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
