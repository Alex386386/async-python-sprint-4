from sqlalchemy import Column, ForeignKey, Integer, DateTime

from app.core.db import Base


class URLAccessLog(Base):
    short_url_id = Column(Integer, ForeignKey('shorturl.id'))
    access_time = Column(DateTime)
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_urlaccesslog_user_id_user'),
        nullable=True
    )
