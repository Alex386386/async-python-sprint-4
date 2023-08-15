from http import HTTPStatus
from typing import List, Optional, Union, Dict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_the_unique_url,
    check_url_name,
    check_exists,
    check_the_opportunity_to_update, check_the_opportunity_to_use,
)
from app.core.db import get_async_session
from app.core.user import current_user, fastapi_users
from app.crud.shorturl import short_url_crud
from app.crud.url_access import access_crud
from app.models import User, ShortURL
from app.schemas.shorturl import ShortURLDB, ShortURLCreate, ShortURLBase
from app.schemas.url_access import AccessLogDB

router = APIRouter()


@router.get(
    '/{short_id}/status',
    response_model=Union[dict, List[AccessLogDB]],
)
async def get_url_status(
        short_id: str,
        full_info: bool = Query(False, alias='full-info'),
        max_result: Optional[int] = Query(
            100, gt=0, alias='max-result'),
        offset: Optional[int] = Query(None, ge=0),
        session: AsyncSession = Depends(get_async_session),
) -> Union[dict, List[AccessLogDB]]:
    url = await check_url_name(short_id=short_id, session=session)
    url_id = url.id
    urls = await access_crud.get_by_short_id(short_id=url_id, session=session)
    if full_info:
        return urls[offset:max_result]
    return {'Number_of_calls': len(urls)}


@router.get(
    '/{short_id}',
    status_code=HTTPStatus.TEMPORARY_REDIRECT,
)
async def redirect_by_short_url(
        short_id: str,
        user: Optional[User] = Depends(fastapi_users.current_user(
            active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session),
) -> Dict[str, str]:
    url = await check_url_name(short_id=short_id, session=session)
    await check_the_opportunity_to_use(user, url)
    url_id = url.id
    original_url = str(url.original_url)
    await access_crud.create_url_access(
        short_id=url_id,
        user=user,
        session=session
    )
    return {'Location': original_url}


@router.post(
    '/',
    response_model=ShortURLDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.CREATED,
)
async def create_short_url(
        short_url: ShortURLCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> ShortURL:
    await check_the_unique_url(short_url.original_url, session)
    return await short_url_crud.create_short_url(
        short_url, user, session
    )


@router.patch(
    '/{short_url_id}',
    response_model=ShortURLDB,
)
async def partially_update_meeting_room(
        *,
        short_url_id: int = Query(..., ge=0),
        obj_in: ShortURLBase,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> ShortURL:
    short_url = await check_exists(short_url_id, session)
    await check_the_opportunity_to_update(short_url.user_id, user.id)
    return await short_url_crud.update_url(
        short_url, obj_in, session
    )
