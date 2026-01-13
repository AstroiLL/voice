# Text Receiver

Simple GUI application for Linux that receives text from external applications via HTTP and displays it in an editable window.

## Features

- Receive text via HTTP POST requests
- Edit text directly in the window
- Copy text to clipboard with one click
- Clear text button
- Status bar showing current state
- Two modes: replace existing text or append to it

## Installation

**Note:** Always use `uv` for dependency management in this project.

```bash
# Install dependencies
uv pip install flask
```

## Running

```bash
python main.py
```

The application will open a small window and start an HTTP server on port 5000.

## API

### POST /text

Send text to the application.

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
