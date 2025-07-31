import sqlalchemy
import sqlalchemy.ext.declarative
import typing

Base = sqlalchemy.ext.declarative.declarative_base()

class EventEPTVPresence(Base):
    __tablename__ = "event_eptv_presence"
    __table_args__ = {"schema": "eptv"}
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("eptv.event_eptv.id"), nullable=False)
    event_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __init__(self, event_id: int, user_id: int, content: typing.Optional[str] = None):
        self.event_id = event_id
        self.user_id = user_id
        self.content = content
