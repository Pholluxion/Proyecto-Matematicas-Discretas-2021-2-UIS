# Install all dependencies: pip install -r requirements.txt

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def root():
    return render_template("sign-in/index.html")


@app.route("/messages")
def messages():
    return "Messages"


if __name__ == "__main__":
    root()
