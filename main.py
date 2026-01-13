from flask import Flask, request, jsonify, render_template_string, Response
import queue

app = Flask(__name__)

# Store current text in memory
current_text = ""
# Queue for SSE clients
clients = []

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
            background: #0d0d0d;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 700px;
            background: #1a1a1a;
            border-radius: 16px;
            padding: 28px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.5);
            border: 1px solid #2a2a2a;
        }
        h1 {
            color: #f5f5f5;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
        }
        .status {
            color: #6b7280;
            font-size: 0.85rem;
            margin-bottom: 16px;
        }
        .status.received {
            color: #3b82f6;
        }
        textarea {
            width: 100%;
            min-height: 220px;
            background: #0d0d0d;
            color: #e5e5e5;
            border: 1px solid #2a2a2a;
            border-radius: 10px;
            padding: 16px;
            font-size: 0.95rem;
            line-height: 1.6;
            resize: vertical;
            outline: none;
            transition: border-color 0.15s ease;
        }
        textarea:focus {
            border-color: #3b82f6;
        }
        textarea::placeholder {
            color: #4a4a4a;
        }
        .buttons {
            display: flex;
            gap: 10px;
            margin-top: 16px;
        }
        button {
            padding: 11px 20px;
            font-size: 0.9rem;
            font-weight: 500;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .copy-btn {
            background: #3b82f6;
            color: white;
            flex: 1;
        }
        .copy-btn:hover {
            background: #2563eb;
        }
        .copy-btn:active {
            transform: scale(0.98);
        }
        .copy-btn.copied {
            background: #10b981;
        }
        .clear-btn {
            background: #2a2a2a;
            color: #a3a3a3;
        }
        .clear-btn:hover {
            background: #3a3a3a;
            color: #d4d4d4;
        }
        .clear-btn:active {
            transform: scale(0.98);
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

        // Listen for server-sent events (new text)
        const eventSource = new EventSource('/events');

        eventSource.onmessage = function(event) {
            textArea.value = event.data;
            status.textContent = `Text received (${event.data.length} chars)`;
            status.classList.add('received');
        };
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/events')
def events():
    """SSE endpoint for pushing new text to clients"""
    def event_stream():
        q = queue.Queue()
        clients.append(q)
        try:
            while True:
                text = q.get()
                yield f"data: {text}\n\n"
        except GeneratorExit:
            clients.remove(q)
    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/text', methods=['POST'])
def receive_text():
    """Endpoint to receive text via HTTP POST"""
    global current_text, clients

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    current_text = data['text']

    # Push to all connected clients
    for client in clients[:]:
        try:
            client.put_nowait(current_text)
        except:
            clients.remove(client)

    return jsonify({'status': 'success', 'length': len(current_text)}), 200


def main():
    from waitress import serve
    print("Server running on http://localhost:5000")
    serve(app, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
