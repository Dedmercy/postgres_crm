from app import app
from flask import render_template


@app.errorhandler(403)
def not_enough_right():
    render_template('403.html'), 403
