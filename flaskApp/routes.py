import re

from flask import (redirect, render_template, url_for, session)

from flaskApp import app
from manager import Manager

mgr = Manager()


@app.before_first_request
def before_first_request_func():
    # This function will run once
    session.clear()


@app.route('/')
def index():
    return render_template('experiment/index.html')


@app.route('/end')
def end():
    """Clear the current session, including the stored user id."""
    session.clear()
    return render_template("experiment/end.html")


def process_input(data):
    # remove everything that is not a word followed by a space
    data['msg'] = re.sub(r'[^\w\s]', ' ', data['msg'])
    # replace multiple subsequent white spaces with only one
    data['msg'] = re.sub(' +', ' ', data['msg'])
    mgr.process(data)

    return redirect(url_for('index'))




