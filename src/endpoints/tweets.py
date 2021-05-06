from flask import Blueprint, jsonify, request, current_app
from src import db
from src.api_spec import TweetSchema
from src.models import Tweet
from marshmallow import ValidationError

tweets = Blueprint(name="tweets", import_name=__name__)

x = 5
tweet_schema = TweetSchema()


@tweets.route('/', methods=["POST"])
def post_tweet():
    """
    ---
    post:
      description: Add a new tweet to the database
      requestBody:
        required: true
        content:
            application/json:
                schema: TweetSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
        '405':
          description: invalid input
          content:
            application/json:
              schema: OutputSchema
        '400':
          description: no data provided
          content:
            application/json:
              schema: OutputSchema
      tags:
          - Tweets
    """
    # # retrieve body data from input JSON
    data = request.get_json()
    if not data:
        current_app.logger.error("No JSON payload detected")
        return {"msg": "No input data provided"}, 400
    try:
        serial_data = tweet_schema.load(data)
    except ValidationError as e:
        current_app.logger.error("Data doesn't match")
        return e.messages, 422
    twt_id = serial_data["twitter_id"]
    twt = Tweet.query.filter_by(twitter_id=twt_id).first()
    if not twt:
        serial_data["media_url"] = ", ".join(serial_data["media_url"])
        twt = Tweet(**serial_data)
        current_app.logger.debug(twt)
        db.session.add(twt)
    db.session.commit()
    current_app.logger.info("Tweets successfully added")
    output = {"msg": "Tweet stored in database!"}
    return jsonify(output)


@tweets.route('/allTweets', methods=["GET"])
def list_all_tweets():
    """
    ---
    get:
      description: Return a list of all tweets
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: TweetShow
      tags:
          - Tweets
    """
    all_twts = Tweet.query.all()
    serial_twts = [{'tweet_id': twt.tweet_id,
                    'handle': twt.handle,
                    'text': twt.text,
                    'timestamp': twt.timestamp} for twt in all_twts]
    return jsonify({"tweet_show": serial_twts})


@tweets.route('/test', methods=['GET'])
def test():
    """
    ---
    get:
      description: test endpoint
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - Tweets
    """
    output = {"msg": "I'm the test endpoint from tweets."}
    return jsonify(output)


@tweets.route('/plus', methods=['POST'])
def plus_x():
    """
    ---
    post:
      description: increments the input by x
      requestBody:
        required: true
        content:
            application/json:
                schema: InputSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - Tweets
    """
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # compute result and return as JSON
    result = in_val + x
    output = {"msg": f"Your result is: '{result}'"}
    return jsonify(output)
