import flask
import flask_mongoengine

db = flask_mongoengine.MongoEngine()


def init_app(app: flask.Flask) -> None:
    db.init_app(app)
    app.session_interface = flask_mongoengine.MongoEngineSessionInterface(db)
