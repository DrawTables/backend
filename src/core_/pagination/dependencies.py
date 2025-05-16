from typing import Annotated

from fastapi import Depends, Query

from src.core_.pagination.schemas import PaginationParams


async def add_pagination_params(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(alias="perPage", default=100, ge=1),
) -> PaginationParams:
    return PaginationParams(
        page=page,
        per_page=per_page,
    )

PaginationParamsDependency = Annotated[PaginationParams, Depends(add_pagination_params)]
