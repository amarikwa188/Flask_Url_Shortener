from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from string import ascii_letters as alpha, digits
import random as rng


app: Flask  = Flask(__name__)


def generate_key() -> str:
    key_letters: list[str] = rng.choices(alpha+digits, k=5)
    key: str = ''.join(key_letters)
    return key


@app.route("/", methods=["POST", "GET"])
def index() -> str:
    if request.method == "POST":
        # recieve the long url
        long_url: str = request.form["long-url"]

        # generate a unique shortened url key
        key: str = generate_key()

        # store the url and key in a database
        ## pass

        # display the generated url to the user
        return render_template("display.html", url=key)
    else:
        return render_template("index.html")


@app.route("/<key>")
def re(key):
    # search for the corresponding long url in the database

    return redirect("https://google.com")


if __name__ == "__main__":
    app.run(debug=True)