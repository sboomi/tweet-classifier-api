import os


class Config:
    SQLALCHEMY_DATABASE_URI = ("mysql+mysqlconnector://"
                               f"{os.environ.get('MYSQL_ROOT_USER')}"
                               f":{os.environ.get('MYSQL_ROOT_PASSWORD')}"
                               f"@{os.environ.get('DB_HOST')}"
                               f":{os.environ.get('MYSQL_PORT')}"
                               f"/{os.environ.get('MYSQL_DATABASE')}")
    # TODO: disable these when everything is fine
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
