from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from backend import database as db
from backend import auth

from backend.schema import (
    UserInDB,
    ChatUpdate,
    ChatMetadata,
    ChatResponse,
    ChatResponseModel,
    UserResponseModel,
    UserCollection,
    MessageCollection,
    ChatCollection,
    MessageResponse,
    MessageResponseModel,
    SingleChatResponse,
    CreateMessage,
)

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("", response_model=ChatCollection)
def get_chats(session: Session = Depends(db.get_session)):
    """Get a collection of Chats."""

    sort_key = lambda chat: getattr(chat, "name")
    chats = db.get_all_chats(session)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )

@chats_router.get("/{chat_id}", response_model=ChatResponse, response_model_exclude_none=True)
def get_chat_by_id(chat_id: str, session: Session = Depends(db.get_session), include: Optional[list[str]] = Query(None)):
    """Add a new Chat to the database."""

    chat=db.get_chat_by_id(chat_id, session)
    chat_user=chat.owner
    response_data = {
            "meta": ChatMetadata(message_count=len(chat.messages), user_count=len(chat.users)),
            "chat": ChatResponseModel(
                id=chat.id,
                name=chat.name,
                owner=UserResponseModel(
                    id=chat_user.id,
                    username=chat_user.username,
                    email=chat_user.email,
                    created_at=chat_user.created_at
                ),
                created_at=chat.created_at
            )
        }
    if include:
        if 'messages' in include:
            response_data['messages'] = [MessageResponseModel(
                                            id=message.id,
                                            text=message.text,
                                            chat_id=message.chat_id,
                                            user=UserResponseModel(
                                                id=message.user.id,
                                                username=message.user.username,
                                                email=message.user.email,
                                                created_at=message.user.created_at
                                            ),
                                            created_at=message.created_at
                                        ) for message in chat.messages]
        if 'users' in include:
            response_data['users'] = [UserResponseModel(
                                        id=user.id,
                                        username=user.username,
                                        email=user.email,
                                        created_at=user.created_at
                                    ) for user in chat.users]
    return ChatResponse(**response_data)

@chats_router.put("/{chat_id}", response_model=SingleChatResponse)
def update_chat(chat_id: str, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
    """Update a chat."""

    chat=db.update_chat(chat_id, chat_update, session)
    return SingleChatResponse(chat=ChatResponseModel(id=chat.id,
                                                    name=chat.name,
                                                    owner=UserResponseModel(id=chat.owner.id,
                                                                            username=chat.owner.username,
                                                                            email=chat.owner.email,
                                                                            created_at=chat.owner.created_at),
                                                    created_at=chat.created_at))

@chats_router.delete("/{chat_id}", status_code=204)
def delete_chat(chat_id: str, session: Session = Depends(db.get_session)):
    """Delete a chat."""
    db.delete_chat(chat_id, session)

@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_chat_messages(chat_id: str, session: Session = Depends(db.get_session)):
    """Get the messages of a chat."""

    sort_key = lambda message: getattr(message, "created_at")
    messages = db.get_chat_messages(chat_id, session)
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key),
    )

@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_chat_users(chat_id: str, session: Session = Depends(db.get_session)):
    """Get the messages of a chat."""
    
    sort_key = lambda user: getattr(user, "id")
    users = db.get_chat_users(chat_id, session)
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

@chats_router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=201)
def create_chat_message(chat_id: str,
                   text: CreateMessage,
                   session: Session = Depends(db.get_session),
                   user: UserInDB = Depends(auth.get_current_user)):
    """write a message to a chat."""
    message = db.create_message(chat_id, text.text, session, user)
    return MessageResponse(message=MessageResponseModel(id=message.id, text=message.text, chat_id=message.chat_id,
                                                        user=UserResponseModel(id=user.id,
                                                                                username=user.username,
                                                                                email=user.email,
                                                                                created_at=user.created_at),
                                                        created_at=message.created_at))
