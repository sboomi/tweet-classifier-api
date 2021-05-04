import os
import requests
from openapi_spec_validator import validate_spec_url


def test_tweets_test(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'tweets', 'test')
    response = requests.get(endpoint)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "I'm the test endpoint from tweets."


def test_analysis_test(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'analysis', 'test')
    response = requests.get(endpoint)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "I'm the test endpoint from analysis."


def test_tweets_plus(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'path_for_tweets', 'plus')
    payload = {'number': 5}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Your result is: '10'"


def test_tweets_minus(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'path_for_analysis', 'minus')
    payload = {'number': 1000}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Your result is: '0'"


def test_swagger_specification(host):
    endpoint = os.path.join(host, 'api', 'swagger.json')
    validate_spec_url(endpoint)
    # use https://editor.swagger.io/ to fix issues
