"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Create an APISpec
spec = APISpec(
    title="Tweet Classifier",
    version="1.1.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Define schemas


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        if (field_obj.data_key or field_name).startswith("_"):
            field_obj.data_key = (field_obj.data_key or field_name).lstrip("_")
        else:
            field_obj.data_key = camelcase(field_obj.data_key or field_name)


class InputSchema(Schema):
    msg = fields.String(description="The message to enter.", required=True)


class OutputSchema(Schema):
    msg = fields.String(description="Output message", required=True)


class TweetSchema(CamelCaseSchema):
    media_url = fields.List(fields.Url(),
                            description="Embedded media from a tweet",
                            example=[
        "https://pbs.twimg.com/media/XXXXXXXXXXXXXXX.jpg",
        "https://pbs.twimg.com/media/YYYYYYYYYYYYYYY.jpg"
    ])
    tweet_date = fields.DateTime(description="Timestamp of the tweet",
                                 required=True,
                                 format="%a %b %d %H:%M:%S %z %Y")
    twitter_id = fields.Integer(description="Id of the tweet", required=True)
    handle = fields.String(description="Twitter handle of the user", required=True)
    text = fields.String(description="Contents of the tweet (< 280 characters)")
    profile_user = fields.Url(description="Link to the twitter account",
                              required=True)
    name = fields.String(description="Title of the Twitter user", required=True)
    tweet_link = fields.Url(description="Original URL of the tweet", required=True)
    timestamp = fields.DateTime(description="Parsable timestamp of the tweet", required=True)
    query = fields.Url(description="Similar to `profileUser`")
    _type = fields.String(description="Type of research")


class AnalyzedTweetSchema(CamelCaseSchema):
    method = fields.String(description="Analysis specification")
    prediction = fields.Float(description="Percentage of the prediction")
    analysis_result = fields.String(description="Returned label")
    original_tweet = fields.Nested(TweetSchema(only=('twitter_id', 'handle', 'text')))


# register schemas with spec
spec.components.schema("Input", schema=InputSchema)
spec.components.schema("Output", schema=OutputSchema)
spec.components.schema("Tweet", schema=TweetSchema)
spec.components.schema("AnalyzedTweet", schema=AnalyzedTweetSchema)

# add swagger tags that are used for endpoint annotation
tags = [

    {
        'name': "Tweets",
        "description": "Return tweets"
    },
    {
        'name': 'Analysis',
        'description': 'Get sentiment analysis for tweets'
    },
    {
        'name': "Pipeline",
        'description': 'Queue a model and download your result'
    }
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)