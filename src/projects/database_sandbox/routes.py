from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4

from src.auth.tokens.dependencies import is_verified_user
from src.projects.database_sandbox.database_handlers import (
        create_sandbox_database,
        drop_sandbox_database,
        send_query_to_sandbox
)

ROUTER_V1_PREFIX = "/api/v1/projects/sandbox"

sandbox_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Projects-Sandbox v1"],
    dependencies=[Depends(is_verified_user)],
)



@sandbox_router_v1.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def create_sandbox(
    version_id: UUID4 = Query(alias="versionId"),
):
    await create_sandbox_database(version_id)
    

@sandbox_router_v1.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_sandbox_database(
    version_id: UUID4 = Query(alias="versionId"),
):
    await drop_sandbox_database(str(version_id))
    
    
@sandbox_router_v1.post(
    path="/query",
)
async def send_query(
    query: str,
    version_id: UUID4 = Query(alias="versionId"),
):
    response = await send_query_to_sandbox(
        query=query,
        database_name=str(version_id),
    )
    print(response.all())