"""Flask Application"""

# load libaries
import datetime as dt
import os
import sys

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from src.api_spec import spec
from src.endpoints.models import models
from src.endpoints.swagger import SWAGGER_URL, swagger_ui_blueprint
# load modules
from src.endpoints.tweets import tweets

# init Flask app
app = Flask(__name__)

# Configure SQL database
mysql_uri = (f"mysql://{os.environ.get('MYSQL_USER')}"
             f":{os.environ.get('MYSQL_PASSWORD')}"
             f"/{os.environ.get('MYSQL_DATABASE')}")
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
db = SQLAlchemy(app)

# Create SQL models here


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(200))
    tweet_date = db.Column(db.DateTime(), nullable=False,
                           default=dt.datetime.utcnow)
    twitter_id = db.Column(db.Integer, nullable=False, unique=True)
    handle = db.Column(db.String(15), nullable=False, unique=True)
    text = db.Column(db.Text(280), nullable=False)
    profile_user = db.Column(db.String(35), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    tweet_link = db.Column(db.String(65), nullable=False)
    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=dt.datetime.utcnow)
    query = db.Column(db.String(35), nullable=False)
    _type = db.Column(db.String(15), nullable=False, default="tweet")

    def __repr__(self):
        return (f"{self.handle} posted, "
                f"the {self.timestamp.strftime('%Y-%m-%d')} "
                f"at {self.timestamp.strftime('%H:%M:%s')}, the following:\n"
                f"{self.text}")


# register blueprints. ensure that all paths are versioned!
app.register_blueprint(tweets, url_prefix="/api/v1/tweets")
app.register_blueprint(models, url_prefix="/api/v1/models")

# register all swagger documented functions here

with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())


app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
