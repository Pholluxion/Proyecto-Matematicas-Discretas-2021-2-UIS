#Install all dependencies: pip install -r requirements.txt

from flask import Flask


app =  Flask(__name__)


@app.route("/")
def root():
    return "Home"

@app.route("/messages")
def messages():
    return "Messages"

if __name__ == "__main__":
    root()
