from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel


class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)

class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )

class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")

class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class ChatMetadata(BaseModel):
    """Represents metadata for a chat collection."""
    message_count: int
    user_count: int

class UserResponseModel(BaseModel):
    """Represents a response model for a User"""
    id: int
    username: str
    email: str
    created_at: datetime

class UserResponse(BaseModel):
    """Represents an API response for a User"""
    user: UserResponseModel

class MessageResponseModel(BaseModel):
    id: int
    chat_id: int
    text: str
    user: UserResponseModel
    created_at: datetime

class MessageResponse(BaseModel):
    """Represents an API response for a Message"""
    message:MessageResponseModel

class ChatResponseModel(BaseModel):
    id: int
    name: str
    owner: UserResponseModel
    created_at: datetime

class ChatResponse(BaseModel):
    """Represents an API response for a Chat"""
    meta: ChatMetadata
    chat: ChatResponseModel
    messages: Optional[list[MessageResponseModel]] = None
    users: Optional[list[UserResponseModel]] = None

class SingleChatResponse(BaseModel):
    chat: ChatResponseModel
    
class UserUpdate(BaseModel):
    """Represents parameters for updating an User in the system."""
    username: Optional[str] = None
    email: Optional[str] = None

class ChatUpdate(BaseModel):
    """Represents parameters for updating an Chat in the system."""
    name: str

class ChatCollection(BaseModel): 
    """Represents an API response for a collection of Chats."""
    meta: Metadata
    chats: list[ChatResponseModel]

class UserCollection(BaseModel): 
    """Represents an API response for a collection of Users."""
    meta: Metadata
    users: list[UserResponseModel]

class MessageCollection(BaseModel): 
    """Represents an API response for a collection of Messages."""
    meta: Metadata
    messages: list[MessageResponseModel]

class CreateMessage(BaseModel):
    text: str

