from typing import Protocol

from src.core_.repository import IRepository
from src.infrastructure.database.database import async_session_maker
from src.users.user.repositories import UserRepository
from src.projects.project.repositories import ProjectRepository, ProjectRealtionUserRepository
from src.projects.version.repositories import VersionRepository
from src.users.api_token.repositories import ApiTokenRepository
from src.ai_assistant.chat_history.repositories import AssistantChatMessageRepository

class IUnitOfWork(Protocol):
    # Users
    users: IRepository
    api_tokens: IRepository
    
    #Projects
    projects: IRepository
    projects_relation_users: IRepository
    versions: IRepository
    
    #Assistant Chat Messages
    assistant_chat_messages: IRepository
    

class UnitOfWork:
    _session = None

    def __init__(self, database_session=None):
        if database_session is not None:
            self._session = database_session

    async def __aenter__(self):
        if self._session is None:
            self._session = async_session_maker()

        # Users
        self.users = UserRepository(self._session)
        self.api_tokens = ApiTokenRepository(self._session)
        
        # Projects
        self.projects = ProjectRepository(self._session)
        self.projects_relation_users = ProjectRealtionUserRepository(self._session)
        self.versions = VersionRepository(self._session)
        
        #Assistant Chat Messages
        self.assistant_chat_messages = AssistantChatMessageRepository(self._session)
        
    async def __aexit__(self, *args):
        await self.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def flush(self):
        await self._session.flush()

    async def rollback(self):
        await self._session.rollback()
