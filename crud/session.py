from pydantic import BaseModel
from uuid import UUID
from core.session import InMemoryBackend


class SessionData(BaseModel):
    session: str


inmemory_session = InMemoryBackend[UUID, SessionData]()


async def create_session(user_uuid, session_id):
    data = SessionData(session=str(session_id))
    await inmemory_session.create(user_uuid, data)
    return "created session"


async def read_session(user_uuid, session_id):
    data = SessionData(session=str(session_id))
    return await inmemory_session.read(user_uuid, data)


async def read_session_value(id):
    return await inmemory_session.read_value(id)


async def delete_session(user_uuid):
    await inmemory_session.delete(user_uuid)
    return "deleted session"


async def update_session(id, model):
    await inmemory_session.update(id, model)
    return "updated session"
