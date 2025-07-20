from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/add", methods=["GET"])
def add():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify(result=a + b)

@app.route("/subtract", methods=["GET"])
def subtract():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify(result=a - b)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="healthy")

@app.route("/")
def home():
    return "Welcome to Calculator Web App! Use /add?a=5&b=2"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
