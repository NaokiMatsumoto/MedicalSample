# __init__.py
import os
from flask import Flask
# from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__name__))
# db = SQLAlchemy()
# migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysite'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from medical.views import bp
    app.register_blueprint(bp)
    # app.add_template_filter(replace_newline)
    # db.init_app(app)
    # migrate.init_app(app, db)
    # login_manager.init_app(app)
    return app