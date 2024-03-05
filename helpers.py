import re

from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    # decorate routes to require login.
    # ref: https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/ & cs50 pset9

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def error_message(message, code=400):
    #Render error message page to user.
    def escape(s):
        # escape special characters.
        # ref: https://github.com/jacebrowning/memegen#special-characters & cs50 pset9

        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", top=code, bottom=escape(message)), code

def get_countries(all):
    countries = []
    for country in all:
        countries.append({"name": country.name, "flag": country.flag})
    return countries


def check_email(email):
    # pass the regular expression
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False
