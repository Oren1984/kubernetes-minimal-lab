# Simple Flask application for the Kubernetes minimal lab

from flask import Flask
import os

app = Flask(__name__)

@app.get("/")
def hello():
    return {"message": "Hello, Kubernetes!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
