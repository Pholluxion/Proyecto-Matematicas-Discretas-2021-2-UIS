from distutils.log import debug
from flask import Flask


app =  Flask(__name__)


@app.route("/")
def root():
    return "Home"



if __name__ == "__main__":
    root()
