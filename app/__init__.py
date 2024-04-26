from flask import Flask

app = Flask(__name__)
app.secret_key = "sessionkey" # Should be some random key
app.jinja_env.auto_reload = True
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
from app import routes

