from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.shorturl import short_url_crud
from app.models import ShortURL, User


async def check_the_unique_url(
        url: str,
        session: AsyncSession,
) -> None:
    url_id = await short_url_crud.get_project_id_by_name(url, session)
    if url_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='На эту ссылку уже существует короткая ссылка!',
        )


async def check_url_name(
        short_id: str,
        session: AsyncSession,
) -> ShortURL:
    url = await short_url_crud.get_url_by_short(
        short_id=short_id, session=session)
    if not url:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Объект не существует!'
        )
    return url


async def check_exists(
        obj_id: int,
        session: AsyncSession,
) -> ShortURL:
    model_object = await short_url_crud.get(obj_id, session)
    if model_object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Объект не существует!'
        )
    return model_object


async def check_the_opportunity_to_update(
        short_url_user_id: int,
        user_id: int
) -> None:
    if short_url_user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Редактировать можно только свои url!.'
        )


async def check_the_opportunity_to_use(
        user: Optional[User],
        url: ShortURL,
):
    if user is None and url.type == 'private':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Вы не можете воспользоваться данной ссылкой.',
        )
    elif user is not None and user.id != url.user_id and url.type == 'private':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Вы не можете воспользоваться данной ссылкой.',
        )
