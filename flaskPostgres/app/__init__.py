from flask import Flask, session, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy

# TODO: давай удалим типы? их как правило тут не ставят
app: Flask = Flask(__name__)
db: SQLAlchemy = SQLAlchemy()
app.config.from_object(Config)

# TODO: это зачем?
db.init_app(app)


def my_render_template(template, *args: tuple, **kwargs):
    kwargs['session'] = session
    args = list(args)
    args.insert(0, template)
    return render_template(*args, **kwargs)


from app import routes

app.run(host='0.0.0.0', port=5000, debug=True)
