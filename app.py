from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Serve the snake.py file when the user visits the root URL
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'snake.py')

# Serve other files like images, music, and docs directly from the main folder
@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)
