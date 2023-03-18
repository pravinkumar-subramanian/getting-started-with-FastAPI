"""InMemoryBackend implementation."""
from typing import Dict, Generic, TypeVar
from pydantic import BaseModel
from fastapi import HTTPException, status


ID = TypeVar("ID")
SessionModel = TypeVar("SessionModel", bound=BaseModel)

ALREADY_LOGGED_IN = "You have logged into another device. Continue the session there or refresh the page and relogin here"
SESSION_CLOSED = "Session Terminated. Login again"


class InMemoryBackend(Generic[ID, SessionModel]):
    def __init__(self) -> None:
        """Initialize a new in-memory database."""
        self.data: Dict[ID, SessionModel] = {}

    async def create(self, user_uuid: ID, data: SessionModel):
        """Create a new session entry"""
        self.data[user_uuid] = data.copy(deep=True)

    async def read(self, user_uuid: ID, data: SessionModel):
        """Read an existing session data"""
        user_session = self.data.get(user_uuid)
        if not user_session:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail=SESSION_CLOSED)
        elif user_session.session != data.session:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail=ALREADY_LOGGED_IN)
        return user_session.copy(deep=True)

    async def read_value(self, id: ID):
        """Read an existing session data"""
        value = self.data.get(id)
        return value.session

    async def delete(self, user_uuid: ID) -> None:
        """Delete an exisitng session"""
        del self.data[user_uuid]

    async def update(self, user_uuid: ID, data: SessionModel) -> None:
        """Update an existing session"""
        if self.data.get(user_uuid):
            self.data[user_uuid] = data
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="session does not exist, cannot update")
