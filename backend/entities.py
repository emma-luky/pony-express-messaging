from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    """Represents parameters for creating a User in the system."""
    id: int

class ChatUpdate(BaseModel):
    """Represents parameters for updating an Chat in the system."""
    name: str

class Message(BaseModel): 
    """Represents an API response for a collection of Messages."""
    id: int
    user_id: str
    text: str
    created_at: datetime

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int


class MessageCollection(BaseModel): 
    """Represents an API response for a collection of Messages."""
    meta: Metadata
    messages: list[Message]

# class UserResponse(BaseModel):
#     """Represents an API response for a User"""
#     user: User

# class ChatResponse(BaseModel):
#     """Represents an API response for a User"""
#     chat: Chat