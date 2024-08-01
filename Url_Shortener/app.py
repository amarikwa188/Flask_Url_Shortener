from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from string import ascii_letters as alpha, digits
import random as rng


# create an instance of a flask application
app: Flask  = Flask(__name__)

# set database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///binds.db"
# set modifications to false
app.config["SQLALHEMY_TRACK_MODIFICATIONS"] = False

# initialize database object
db: SQLAlchemy = SQLAlchemy(app)

# create table class
class URL_Binds(db.Model):
    """
    Represents a table in the database.
    """
    short_url = db.Column(db.String(10), primary_key=True)
    long_url = db.Column(db.String(100), nullable=False)

    def __init__(self, short, long):
        self.short_url = short
        self.long_url = long 

    def __repr__(self) -> str:
        return f"{self.long_url}::{self.short_url}"
    

def generate_key() -> str:
    """
    Generate a 5 character key to serve as the shortened url.

    :return: 5 character key
    """
    key_letters: list[str] = rng.choices(alpha+digits, k=5)
    key: str = ''.join(key_letters)
    return key


@app.route("/", methods=["POST", "GET"])
def index() -> str:
    """
    The main page accepts long urls as well as displays shortened urls.
    """
    if request.method == "POST":
        # recieve the long url
        long_url: str = request.form["long-url"]

        # generate a shortened url key
        key: str = generate_key()

        # search the database to make sure the key is unique
        binds: list[str] = [str(x) for x in URL_Binds.query.all()]

        used_keys: list[str] = []
        for record in binds:
            short = record.split("::")[1]
            used_keys.append(short)

        while key in used_keys:
            key = generate_key()            

        # store the url and key in a database
        url_bind: URL_Binds = URL_Binds(key, long_url)
        try:
            db.session.add(url_bind)
            db.session.commit()
        except Exception as e:
            print(e.with_traceback(None))

        # display the generated url to the user
        return render_template("display.html", url=key)
    else:
        # return main page
        return render_template("index.html")


@app.route("/<key>")
def re(key):
    """
    Redirects to the approriate web page using the short url key.
    """
    # search for the corresponding long url in the database
    binds: list[str] = [str(x) for x in URL_Binds.query.all()]
    for record in binds:
        long, short = record.split("::")
        if short != key:
            continue

        if not long.startswith(('http://', 'https://')):
            long = 'http://' + long

        return redirect(long)
        
    return "Page Not Found"


@app.route("/delete_all_binds")
def delete():
    """
    Delete all contents of the database.
    """
    print(f"\n{URL_Binds.query.all()}\n")

    for bind in URL_Binds.query.all():
        db.session.delete(bind)
    db.session.commit()

    print(f"\n{URL_Binds.query.all()}\n")

    return "<p style='color: red;'>Database Cleared</p>"


@app.route("/check_all_binds")
def check():
    """
    Check all url binds in the database.
    """
    display: str = ''

    for bind in URL_Binds.query.all():
        display += f"{bind}\n"

    return display


if __name__ == "__main__":
    # create the database
    with app.app_context():
        db.create_all()
    
    # run the application
    app.run(debug=True)
