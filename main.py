import threading
import tkinter as tk
from tkinter import scrolledtext
from queue import Queue

# CRITICAL: Initialize Tkinter BEFORE importing Flask
# This prevents XInitThreads conflict
root = tk.Tk()
root.withdraw()  # Hide initially

# Now it's safe to import Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global queue for thread communication
text_queue = Queue()


class TextReceiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Receiver")
        self.root.geometry("500x300")

        # Label
        self.label = tk.Label(root, text="Received text:", font=("Arial", 10))
        self.label.pack(pady=5)

        # Text area with scrollbar
        self.text_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=60,
            height=12,
            font=("Arial", 11)
        )
        self.text_area.pack(padx=10, pady=5, expand=True, fill='both')

        # Copy button
        self.copy_button = tk.Button(
            root,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=("Arial", 10)
        )
        self.copy_button.pack(pady=5)

        # Clear button
        self.clear_button = tk.Button(
            root,
            text="Clear",
            command=self.clear_text,
            font=("Arial", 10)
        )
        self.clear_button.pack(pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Server running on http://localhost:5000")
        self.status_bar = tk.Label(
            root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_text(self, text):
        """Set text in the text area"""
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)
        self.status_var.set(f"Text received ({len(text)} chars)")

    def append_text(self, text):
        """Append text to the existing text"""
        self.text_area.insert(tk.END, text)
        self.status_var.set(f"Text appended ({len(text)} chars)")

    def copy_to_clipboard(self):
        """Copy selected text or all text to clipboard"""
        text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST) if self.text_area.tag_ranges(tk.SEL) else self.text_area.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text.strip())
        self.status_var.set("Copied to clipboard")

    def clear_text(self):
        """Clear the text area"""
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("Cleared")


@app.route('/text', methods=['POST'])
def receive_text():
    """Endpoint to receive text via HTTP POST"""
    global text_queue

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    mode = data.get('mode', 'set')  # 'set' to replace, 'append' to add

    text_queue.put(('set', text) if mode == 'set' else ('append', text))

    return jsonify({'status': 'success', 'length': len(text)}), 200


@app.route('/text', methods=['GET'])
def get_text():
    """Endpoint to get current text via HTTP GET"""
    return jsonify({'text': 'Use GUI to view text'}), 200


def run_flask():
    """Run Flask server using waitress (no X11 conflicts)"""
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=1)


def check_queue(gui_app):
    """Check for incoming text and update GUI"""
    try:
        while True:
            mode, text = text_queue.get_nowait()
            if mode == 'set':
                gui_app.set_text(text)
            else:
                gui_app.append_text(text)
    except:
        pass
    finally:
        # Check again after 100ms
        gui_app.root.after(100, lambda: check_queue(gui_app))


def main():
    # Start Flask server in a separate thread (daemon, so it exits when main exits)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Configure and show the pre-initialized root
    root.deiconify()  # Show the window
    gui_app = TextReceiverApp(root)

    # Start checking queue
    root.after(100, lambda: check_queue(gui_app))

    root.mainloop()


if __name__ == "__main__":
    main()
