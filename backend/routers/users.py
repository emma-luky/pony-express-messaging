from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend import database as db
from backend import auth

from backend.schema import (
    UserResponseModel,
    UserInDB,
    UserResponse,
    UserUpdate,
    UserCollection,
    ChatCollection
)

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/me", response_model=UserResponse)
def get_me(session: Session = Depends(db.get_session),
                   user: UserInDB = Depends(auth.get_current_user)):
    """Retrieves the current logged in user."""
    if user:
        return UserResponse(user=UserResponseModel(id=user.id, username=user.username, email=user.email, created_at=user.created_at))

@users_router.put("/me", response_model=UserResponse)
def update_me(user_update: UserUpdate,
                session: Session = Depends(db.get_session),
                user: UserInDB = Depends(auth.get_current_user)):
    """Update a current user's username or email."""
    user = db.update_user(user, user_update, session)
    if user:
        return UserResponse(user=UserResponseModel(id=user.id, username=user.username, email=user.email, created_at=user.created_at))

@users_router.get("", response_model=UserCollection)
def get_users(session: Session = Depends(db.get_session)):
    """Retrives all users within the database."""
    
    sort_key = lambda user: getattr(user, "id")
    users = db.get_all_users(session)
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, session: Session = Depends(db.get_session)):
    """Retrieves a user from the database by user_id"""
    user=db.get_user_by_id(user_id, session)
    return UserResponse(user=UserResponseModel(id=user.id, username=user.username, email=user.email, created_at=user.created_at))

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(user_id: str, session: Session = Depends(db.get_session)):
    """Retrieves the chats that the user_id participates in, sorted by chat name."""

    sort_key = lambda chat: getattr(chat, "name")
    chats = db.get_user_chats(user_id, session)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )