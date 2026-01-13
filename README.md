# Text Receiver

Web application that receives text from external applications via HTTP and displays it in a browser-based text editor.

## Features

- Receive text via HTTP POST requests
- Web interface accessible at http://localhost:5000
- Copy text to clipboard with one click
- Clear text button
- Auto-refresh to show incoming text
- Two modes: replace existing text or append to it

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

Send text to the application from any external app.

```bash
curl -X POST http://localhost:5000/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, World!"}'
```

**Parameters:**
- `text` (required): The text to display
- `mode` (optional): `"set"` (default) to replace existing text, `"append"` to add to existing text

**Examples:**

Replace text:
```bash
curl -X POST http://localhost:5000/text \
  -H "Content-Type: application/json" \
  -d '{"text": "New text"}'
```

Append text:
```bash
curl -X POST http://localhost:5000/text \
  -H "Content-Type: application/json" \
  -d '{"text": "\nAdditional line", "mode": "append"}'
```

### GET /text

Get the current text from the application.

```bash
curl http://localhost:5000/text
```

**Response:**
```json
{"text": "Current text content"}
```
