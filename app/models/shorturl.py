from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class ShortURL(Base):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_shorturl_user_id_user')
    )
    short_url = Column(String(100))
    original_url = Column(String(300))
    type = Column(String(10), default='public')
    url_access = relationship('URLAccessLog', cascade='delete')
