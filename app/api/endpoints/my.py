from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.shorturl import short_url_crud
from app.models import User
from app.schemas.shorturl import ShortURLDB

router = APIRouter()


@router.get(
    '/user/status',
    tags=['user'],
    response_model=List[ShortURLDB],
    dependencies=[Depends(current_user)],
)
async def get_url_status(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    accesses = await short_url_crud.get_my(user=user, session=session)
    if not accesses:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Объект не существует!'
        )
    return accesses
