from flask import Blueprint, jsonify, request

models = Blueprint(name="models", import_name=__name__)

y = 1000


@models.route('/test', methods=['GET'])
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
          - Analysis
    """
    output = {"msg": "I'm the test endpoint from models."}
    return jsonify(output)


@models.route('/minus', methods=['POST'])
def minus_y():
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
          - Analysis
    """
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # comput result and output as JSON
    result = in_val - y
    output = {"msg": f"Your result is: '{result}'"}
    return jsonify(output)
