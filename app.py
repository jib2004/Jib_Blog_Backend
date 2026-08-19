from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values

from routes.auth import auth
from routes.blog import blog

from config import db
from exceptions.exceptions import (
    ValidationError,
    AuthenticationError,
    not_found,
    unauthorized,
    handle_validation_error,
    handle_http_exception,
    handle_unexpected_error
)
from werkzeug.exceptions import HTTPException

config = dotenv_values(".env")

app = Flask(__name__)

app.secret_key = config['SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URL"]
db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(blog,url_prefix='/blog')

# ─── Register error handlers here ────────────────────────
app.register_error_handler(404, not_found)
app.register_error_handler(401, unauthorized)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(Exception, handle_unexpected_error)

with app.app_context():
    db.create_all()

if __name__ == '__main__':

    app.run(debug=True)

