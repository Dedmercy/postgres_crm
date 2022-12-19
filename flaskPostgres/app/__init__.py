from flask import Flask, session, render_template
from config import Config

app: Flask = Flask(__name__)
app.config.from_object(Config)

from app import routes

app.run(host='0.0.0.0', port=5000, debug=True)
