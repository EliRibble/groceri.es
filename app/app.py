from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from config import Config
from slugify import slugify
import pycountry

app = Flask(__name__)
app.config.from_object(Config())

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True, render_as_batch=True)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

babel = Babel(app)

from models import User  # noqa
@login_manager.user_loader
def load_user(user_id):
    """Load user with specified user ID."""
    return User.query.get(int(user_id))


from models import Setting  # noqa
@babel.localeselector
def get_locale():
    """Get the selected locale from user settings."""
    setting = Setting.query.filter(Setting.name == 'default_language').first()

    if setting is not None:
        return setting.value

    # Return default language when none found
    return 'en'


@app.template_filter('slugify')
def slug(value):
    """Jinja2 filter to slugify text."""
    return slugify(value)


@app.template_filter('language_name')
def language_name(value):
    """Jinja2 filter to get language object from language code."""
    return pycountry.languages.get(alpha_2=value)


"""Import all web routes and CLI routes to run this app"""
import views, cli  # noqa