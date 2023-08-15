from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import ShortURL, User, URLAccessLog


class CRUDAccessLog(CRUDBase):

    async def create_url_access(
            self,
            short_id: int,
            user: Optional[User],
            session: AsyncSession,
    ) -> None:
        obj_in_data = {
            'short_url_id': short_id,
            'access_time': datetime.now()
        }
        if user:
            obj_in_data['user_id'] = user.id
        db_access = self.model(**obj_in_data)
        session.add(db_access)
        await session.commit()
        await session.refresh(db_access)

    async def get_by_short_id(
            self,
            short_id: int,
            session: AsyncSession,
    ) -> List[ShortURL]:
        urls = await session.execute(
            select(URLAccessLog).where(
                URLAccessLog.short_url_id == short_id
            )
        )
        return urls.scalars().all()


access_crud = CRUDAccessLog(URLAccessLog)
