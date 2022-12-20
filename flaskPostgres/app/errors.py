from app import app
from flask import render_template

from app.routes import parametrized_render_template


@app.errorhandler(403)
def not_enough_right(error):
    parametrized_render_template('403.html'), 403
