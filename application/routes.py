  
from flask import current_app as app
from flask import render_template

from .models import User, Chat, Message
from users.routes import UserAPI

app.register_blueprint(UserAPI, url_prefix='/user')

# homepage
@app.route('/')
def welcome():
    return render_template('...')