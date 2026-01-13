# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Web application that receives text from external applications via HTTP and displays it in a browser-based text editor. Uses Python 3.12+ with Flask and Server-Sent Events for real-time updates.

## Development Commands

### Running the Application

```bash
python main.py
```

Open http://localhost:5000 in your browser.

### Installing Dependencies

```bash
# Using uv (recommended)
uv pip install flask waitress

# Or using pip
pip install flask waitress
```

## Project Structure

- `main.py` - Flask application with SSE support and HTML template
- `pyproject.toml` - Project configuration
- `.python-version` - Specifies Python 3.12

## API

### POST /text

Send text to the application. Text appears in browser in real-time via SSE.

```bash
curl -X POST http://localhost:5000/text \
  -H "Content-Type: application/json" \
  -d '{"text": "your text here"}'
```

## Architecture

- Flask serves the web interface and API endpoints
- Server-Sent Events (SSE) push new text to connected browsers instantly
- Waitress serves the production WSGI server
- HTML/CSS/JS embedded in main.py for single-file deployment
