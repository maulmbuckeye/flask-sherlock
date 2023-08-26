import os
import json
from json.decoder import JSONDecodeError

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from rengine import Sherlock


# Set up app
app = Flask(__name__)
app.json.ensure_ascii = False
APP_DIR = os.path.dirname(os.path.realpath(__file__))


def read_data(source):
    """
    Reads file that is expected to hold JSON encoded content.
    In case of errors return empty data and list holding error message.
    """
    data = []
    errors = []
    try:
        with open(source) as db:
            content = db.read()
        data = json.loads(content)
    except FileNotFoundError as e:
        errors = [f"Reading {source}, {str(e)}"]
    except JSONDecodeError as e:
        errors = [f"Reading {source}, {str(e)}"]
    except Exception as e:
        errors = [f"Reading {source}, {str(e)}"]

    return data, errors


@app.route("/api/v1/movies/recommend", methods=["GET"])
def recommend():
    """
    Function loads movies from db and returns recommendations.
    """
    # noinspection PyPep8Naming
    MOVIES, errors = read_data(f"{APP_DIR}/db.json")
    if errors:
        return jsonify({"errors": errors, "status_code": 500}), 500

    sherlock = Sherlock(MOVIES, request.args)
    recommendation = sherlock.recommend()

    return jsonify(recommendation)


@app.route("/pretty", methods=["GET"])
def pretty():
    """
    Function loads movies from db and returns recommendations.
    """
    # noinspection PyPep8Naming
    MOVIES, errors = read_data(f"{APP_DIR}/db.json")
    if errors:
        return jsonify({"errors": errors, "status_code": 500}), 500

    sherlock = Sherlock(MOVIES, request.args)
    recommendation = sherlock.recommend()

    html = ""
    return render_template('movie_list.html', movies=recommendation)


@app.route("/user/<name>", methods=["GET"])
def root(name):
    return render_template('hello.html', name=name)
