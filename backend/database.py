from datetime import datetime
import json
import os
from sqlmodel import Session, SQLModel, create_engine, select

from fastapi import HTTPException

from backend.schema import (
    UserInDB,
    UserUpdate,
    ChatInDB,
    MessageInDB,
    UserResponseModel,
    ChatResponseModel,
    MessageResponseModel,
    ChatUpdate
)

def get_engine():
    if os.environ.get("DB_LOCATION") == "EFS":
        db_path = "/mnt/efs/pony_express.db"
        echo = False
    else:
        db_path = "backend/pony_express.db"
        echo = True
    return create_engine(
    f"sqlite:///{db_path}",
    echo=echo,
    connect_args={"check_same_thread": False},
    )

engine = get_engine()

# with open("backend/fake_db.json", "r") as f:
#     DB = json.load(f)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

""" users """

def get_all_users(session: Session) -> list[UserResponseModel]:
    """
    Retrieve all users from the database.

    :return: ordered list of Users
    """
    users = session.exec(select(UserInDB)).all()
    return [
        UserResponseModel(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        ) for user in users
    ]

def get_user_by_id(user_id: str, session: Session) -> UserInDB:
    """
    Retrieve an User from the database by ID.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    :raises HTTPException: if no such user exists
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user
    else:
        raise HTTPException(
                status_code=404,
                detail={
                    "type":"entity_not_found",
                    "entity_name":"User",
                    "entity_id":user_id
                }
            )
    
def update_user(user: UserInDB, user_update: UserUpdate, session: Session) -> UserInDB:
    """
    Update an chat in the database for a given ID.

    :param chat_id: id of the Chat to be updated
    :param chat_update: new Chat name
    :return: the updated chat
    :raises HTTPException: if no such chat exists
    """
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    session.commit()
    session.refresh(user)
    return user

def get_user_chats(user_id: str, session: Session) -> list[ChatResponseModel]:
    """
    Retrieves a list of chats for a given User ID.

    :param user_id: the id of the user
    :return a list of chats alongside some metadata
    """
    user = get_user_by_id(user_id, session)
    user_chats = []
    all_chats = session.exec(select(ChatInDB)).all()
    for chat in all_chats:
        if user in chat.users:
            user_chats.append(chat)
    return [
        ChatResponseModel(
            id=chat.id,
            name=chat.name,
            owner=UserResponseModel(
                id=chat.owner.id,
                username=chat.owner.username,
                email=chat.owner.email,
                created_at=chat.owner.created_at
            ),
            created_at=chat.created_at
        ) for chat in user_chats
    ]

""" end users """

""" chats """

def get_all_chats(session: Session) -> list[ChatResponseModel]:
    """
    Retrieve all chats from the database.

    :return: ordered list of Chats
    """
    chats = session.exec(select(ChatInDB)).all()
    return [
        ChatResponseModel(
            id=chat.id,
            name=chat.name,
            owner=UserResponseModel(
                id=chat.owner.id,
                username=chat.owner.username,
                email=chat.owner.email,
                created_at=chat.owner.created_at
            ),
            created_at=chat.created_at
        ) for chat in chats
    ]

def get_chat_by_id(chat_id: str, session: Session) -> ChatInDB:
    """
    Retrieve an chat from the database by hat ID.

    :param chat_id: id of the user to be retrieved
    :return: the retrieved chat
    :raises HTTPException: if no such chat exists
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "type":"entity_not_found",
                "entity_name":"Chat",
                "entity_id":chat_id
            }
        )

def update_chat(chat_id: str, chat_update: ChatUpdate, session: Session) -> ChatInDB:
    """
    Update an chat in the database for a given ID.

    :param chat_id: id of the Chat to be updated
    :param chat_update: new Chat name
    :return: the updated chat
    :raises HTTPException: if no such chat exists
    """
    chat = get_chat_by_id(chat_id, session)
    if chat:
        # chat.name = chat_update.name
        setattr(chat, "name", chat_update.name)
        # session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

def delete_chat(chat_id: str, session: Session):
    """
    Delete an chat from the database.

    :param chat_id: the id of the user to be deleted
    :return: true if delection is succesful, false otherwise
    """
    chat = get_user_by_id(session, chat_id)
    session.delete(chat)
    session.commit()

""" end chats """

""" messages """

def get_chat_messages(chat_id: str, session: Session) -> list[MessageInDB]:
    """
    Retrieves a list of messages for a given chat_id

    :param chat_id: id of the chat
    :return: the retrieved message list
    :raises HTTPException: if no such chat exists
    """
    chat = get_chat_by_id(chat_id, session)
    if chat:
        return [
            MessageResponseModel(
                id=message.id,
                chat_id=message.chat_id,
                text=message.text,
                user=UserResponseModel(
                    id=message.user.id,
                    username=message.user.username,
                    email=message.user.email,
                    created_at=message.user.created_at
                ),
                created_at=message.created_at
            ) for message in chat.messages
        ]
    
def create_message(chat_id: str, text: str, session: Session, user: UserInDB) -> MessageInDB:
    chat = get_chat_by_id(chat_id, session)
    if chat:
        message = MessageInDB(
            text=text,
            user_id=user.id,
            chat_id=chat_id,
            user=user,
            chat=chat
            )
        session.add(message)
        chat.messages.append(message)
        session.commit()
        session.refresh(message)
        return message
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "type":"entity_not_found",
                "entity_name":"Chat",
                "entity_id":chat_id
            }
        )

def get_chat_users(chat_id: str, session: Session) -> list[UserResponseModel]:
    """
    Retrieves a list of users for a given chat_id

    :param chat_id: id of the chat
    :return: the retrieved user list
    :raises HTTPException: if no such chat exists
    """
    chat = get_chat_by_id(chat_id, session)
    if chat:
        users = chat.users
        return [
            UserResponseModel(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            ) for user in users
        ]

""" end chats """