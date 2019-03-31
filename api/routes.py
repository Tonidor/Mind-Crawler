import falcon
from falcon import API
from Resources import *
from Helpers.Middlewares import SQLAlchemySessionManager, Jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///entries.db")#, echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_app() -> API:
    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session), Jsonify(help_messages=True)])
    _app.add_route('/entry', EntryResource())
    _app.add_route('/graph', GraphResource())
    return _app
