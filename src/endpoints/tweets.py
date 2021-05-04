from flask import Blueprint, jsonify, request

tweets = Blueprint(name="tweets", import_name=__name__)

x = 5


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
      tags:
          - Tweets
    """
    # # retrieve body data from input JSON
    # data = request.get_json()
    # in_val = data['number']
    # # compute result and return as JSON
    # result = in_val + x
    output = {"msg": "Tweet stored in database!"}
    return jsonify(output)


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
