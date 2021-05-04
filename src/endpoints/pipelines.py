from flask import Blueprint, jsonify, request

pipelines = Blueprint(name="pipelines", import_name=__name__)


@pipelines.route('/new', methods=['POST'])
def new_pipeline():
    pass
