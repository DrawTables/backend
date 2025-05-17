from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import ProgrammingError
from asyncpg.exceptions import InvalidCatalogNameError
from sqlalchemy.sql import text

from src.infrastructure.database.postgres_ import (
    create_sandbox_postgres_async_engine
)
from src.projects.database_sandbox.utils import convert_dbml_to_sql
from src.projects.version import use_cases


async def create_sandbox_database_connection(
    database_name: str,
) -> AsyncSession:
    try:
        session = await create_sandbox_postgres_async_engine(database_name)
        conn = await session.connect()
        return conn
    except InvalidCatalogNameError as exc:
        session = await create_sandbox_postgres_async_engine("postgres")
        conn = await session.connect()
        await conn.execute(text("commit"))
        await conn.execute(text(f'CREATE DATABASE "{database_name}"'))
        await conn.close()
        session = await create_sandbox_postgres_async_engine(database_name)
        conn = await session.connect()
    return conn
   
        
async def create_sandbox_database(
    version_id: UUID4,
) -> None:
    sandbox_connection = await create_sandbox_database_connection(str(version_id))
    version = await use_cases.get_version(
        version_id=version_id,
    )    
    dbml_text = version.dbml_text
    sql = convert_dbml_to_sql(dbml_text)
    sql_stmts = sql.split("\n\n")
    for sql in sql_stmts:
        await sandbox_connection.execute(text(sql))
    await sandbox_connection.commit()
    await sandbox_connection.close()


async def drop_sandbox_database(
    database_name: str,
) -> None:
    session = create_sandbox_postgres_async_engine("postgres")
    async with session() as conn:
        conn.execute("commit")
        await conn.execute(f"DROP DATABASE {database_name}")
        
        
async def send_query_to_sandbox(
    query: str,
    database_name: str,
):
    session = await create_sandbox_database_connection(database_name)
    stmt = text(query)
    response = await session.execute(stmt)
    return response