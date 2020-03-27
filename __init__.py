"""
The flask application package.
"""

from flask import Flask
from shoplte import custom_config
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

#session configuration
app.config["DEBUG"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = custom_config.secret_key

#create user session
Session(app)

import shoplte.views
