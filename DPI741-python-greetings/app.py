from flask import Flask, jsonify
import argparse

app = Flask(__name__)


@app.route('/greetings')
def greetings():
    return jsonify({"greeting": "Hello from Python App!"})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port')
    args = parser.parse_args()
    app.run(host="127.0.0.1", debug=True, port=args.port)
