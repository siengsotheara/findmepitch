from flask import Flask
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run('0.0.0.0', port=port)