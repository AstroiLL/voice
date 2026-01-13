# Text Receiver

Web application that receives text from external applications via HTTP and displays it in a browser-based text editor.

## Features

- Receive text via HTTP POST requests
- Web interface accessible at http://localhost:5000
- Real-time text updates using Server-Sent Events
- Editable text area
- Copy text to clipboard with one click
- Clear text button

## Installation

**Note:** Always use `uv` for dependency management in this project.

```bash
# Install dependencies
uv pip install flask waitress
```

## Running

```bash
python main.py
```

Open http://localhost:5000 in your browser.

## API

### POST /text

Send text to the application from any external app. Text will appear in the browser in real-time.

```bash
curl -X POST http://localhost:5000/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, World!"}'
```

**Parameters:**
- `text` (required): The text to display
