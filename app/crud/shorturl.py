from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import generate_unique_id
from app.crud.base import CRUDBase
from app.models import ShortURL, User


class CRUDShortURL(CRUDBase):

    async def create_short_url(
            self,
            obj_in,
            user: User,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()

        obj_in_data['user_id'] = user.id
        unique_id = generate_unique_id()
        obj_in_data['short_url'] = unique_id
        if not obj_in_data['type']:
            obj_in_data['type'] = 'public'
        db_donation = self.model(**obj_in_data)

        session.add(db_donation)
        await session.commit()
        await session.refresh(db_donation)
        return db_donation

    async def update_url(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_url_by_short(
            self,
            short_id: str,
            session: AsyncSession,
    ) -> Optional[str]:
        url = await session.execute(
            select(ShortURL).where(
                ShortURL.short_url == short_id
            )
        )
        return url.scalars().first()

    async def get_project_id_by_name(
            self,
            url: str,
            session: AsyncSession,
    ) -> Optional[ShortURL]:
        url = await session.execute(
            select(ShortURL.id).where(
                ShortURL.original_url == url
            )
        )
        return url.scalars().first()

    async def get_my(
            self,
            user: User,
            session: AsyncSession,
    ) -> List[ShortURL]:
        urls = await session.execute(
            select(ShortURL).where(
                ShortURL.user_id == user.id
            )
        )
        return urls.scalars().all()


short_url_crud = CRUDShortURL(ShortURL)
