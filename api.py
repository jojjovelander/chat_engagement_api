from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import *

# Pydantic models for request/response serialization
from pydantic import BaseModel


# Role models
class RoleBase(BaseModel):
    Name: str


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    Id: int

    class Config:
        orm_mode = True


# User models
class UserBase(BaseModel):
    Name: str
    UserId: str
    Email: str
    RoleId: int


class UserCreate(UserBase):
    LoginToken: Optional[int] = None


class UserResponse(UserBase):
    Id: int
    LoginToken: Optional[int]
    CreatedUtc: str
    LastAccessedUtc: str

    class Config:
        orm_mode = True


class UserWithRole(UserResponse):
    role: RoleResponse

    class Config:
        orm_mode = True


# Group models
class GroupBase(BaseModel):
    Id: str
    Name: str
    Assistant: str
    Active: bool


class GroupCreate(GroupBase):
    pass


class GroupResponse(GroupBase):
    class Config:
        orm_mode = True


# Thread models
class ThreadBase(BaseModel):
    Id: str
    UserId: int
    Title: str
    GroupId: Optional[str] = None


class ThreadCreate(ThreadBase):
    pass


class ThreadResponse(ThreadBase):
    Created: str

    class Config:
        orm_mode = True


# Image models
class ImageBase(BaseModel):
    Id: str
    ThreadId: str
    Data: str


class ImageCreate(ImageBase):
    pass


class ImageResponse(ImageBase):
    class Config:
        orm_mode = True


# Message models
class MessageBase(BaseModel):
    ThreadId: str
    Text: str
    Role: int


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    Id: int
    Created: str

    class Config:
        orm_mode = True


# UserGroup models
class UserGroupBase(BaseModel):
    Id: str
    UserId: int
    GroupId: str


class UserGroupCreate(UserGroupBase):
    pass


class UserGroupResponse(UserGroupBase):
    class Config:
        orm_mode = True


# Models with relationships
class ThreadWithRelations(ThreadResponse):
    user: UserResponse
    group: Optional[GroupResponse] = None
    messages: List[MessageResponse] = []
    images: List[ImageResponse] = []

    class Config:
        orm_mode = True


class GroupWithRelations(GroupResponse):
    threads: List[ThreadResponse] = []
    user_groups: List[UserGroupResponse] = []

    class Config:
        orm_mode = True


class UserWithRelations(UserResponse):
    role: RoleResponse
    threads: List[ThreadResponse] = []
    user_groups: List[UserGroupResponse] = []

    class Config:
        orm_mode = True


engine = create_engine("sqlite:///local.db", echo=True)
session = Session(engine)


# Database dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# API endpoints
def create_api_router(app: FastAPI):
    # Role endpoints
    @app.post("/roles/", response_model=RoleResponse)
    def create_role(role: RoleCreate, db: Session = Depends(get_db)):
        db_role = Role(Name=role.Name)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    @app.get("/roles/", response_model=List[RoleResponse])
    def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        roles = db.scalars(select(Role).offset(skip).limit(limit)).all()
        return roles

    @app.get("/roles/{role_id}", response_model=RoleResponse)
    def read_role(role_id: int, db: Session = Depends(get_db)):
        role = db.get(Role, role_id)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    # User endpoints
    @app.post("/users/", response_model=UserResponse)
    def create_user(user: UserCreate, db: Session = Depends(get_db)):
        import datetime
        now = datetime.datetime.utcnow().isoformat()
        db_user = User(
            Name=user.Name,
            UserId=user.UserId,
            LoginToken=user.LoginToken,
            Email=user.Email,
            RoleId=user.RoleId,
            CreatedUtc=now,
            LastAccessedUtc=now
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @app.get("/users/", response_model=List[UserResponse])
    def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = db.scalars(select(User).offset(skip).limit(limit)).all()
        return users

    @app.get("/users/{user_id}", response_model=UserResponse)
    def read_user(user_id: int, db: Session = Depends(get_db)):
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @app.get("/users/{user_id}/with-role", response_model=UserWithRole)
    def read_user_with_role(user_id: int, db: Session = Depends(get_db)):
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @app.get("/users/{user_id}/with-relations", response_model=UserWithRelations)
    def read_user_with_relations(user_id: int, db: Session = Depends(get_db)):
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    # Group endpoints
    @app.post("/groups/", response_model=GroupResponse)
    def create_group(group: GroupCreate, db: Session = Depends(get_db)):
        db_group = Group(
            Id=group.Id,
            Name=group.Name,
            Assistant=group.Assistant,
            Active=group.Active
        )
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group

    @app.get("/groups/", response_model=List[GroupResponse])
    def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        groups = db.scalars(select(Group).offset(skip).limit(limit)).all()
        return groups

    @app.get("/groups/{group_id}", response_model=GroupResponse)
    def read_group(group_id: str, db: Session = Depends(get_db)):
        group = db.get(Group, group_id)
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")
        return group

    @app.get("/groups/{group_id}/with-relations", response_model=GroupWithRelations)
    def read_group_with_relations(group_id: str, db: Session = Depends(get_db)):
        group = db.get(Group, group_id)
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")
        return group

    # Thread endpoints
    @app.post("/threads/", response_model=ThreadResponse)
    def create_thread(thread: ThreadCreate, db: Session = Depends(get_db)):
        import datetime
        now = datetime.datetime.utcnow().isoformat()
        db_thread = Thread(
            Id=thread.Id,
            UserId=thread.UserId,
            Title=thread.Title,
            GroupId=thread.GroupId,
            Created=now
        )
        db.add(db_thread)
        db.commit()
        db.refresh(db_thread)
        return db_thread

    @app.get("/threads/", response_model=List[ThreadResponse])
    def read_threads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        threads = db.scalars(select(Thread).offset(skip).limit(limit)).all()
        return threads

    @app.get("/threads/{thread_id}", response_model=ThreadResponse)
    def read_thread(thread_id: str, db: Session = Depends(get_db)):
        thread = db.get(Thread, thread_id)
        if thread is None:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    @app.get("/threads/{thread_id}/with-relations", response_model=ThreadWithRelations)
    def read_thread_with_relations(thread_id: str, db: Session = Depends(get_db)):
        thread = db.get(Thread, thread_id)
        if thread is None:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    # Message endpoints
    @app.post("/messages/", response_model=MessageResponse)
    def create_message(message: MessageCreate, db: Session = Depends(get_db)):
        import datetime
        now = datetime.datetime.utcnow().isoformat()
        db_message = Message(
            ThreadId=message.ThreadId,
            Text=message.Text,
            Role=message.Role,
            Created=now
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @app.get("/messages/", response_model=List[MessageResponse])
    def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        messages = db.scalars(select(Message).offset(skip).limit(limit)).all()
        return messages

    @app.get("/messages/{message_id}", response_model=MessageResponse)
    def read_message(message_id: int, db: Session = Depends(get_db)):
        message = db.get(Message, message_id)
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return message

    # Image endpoints
    @app.post("/images/", response_model=ImageResponse)
    def create_image(image: ImageCreate, db: Session = Depends(get_db)):
        db_image = Image(
            Id=image.Id,
            ThreadId=image.ThreadId,
            Data=image.Data
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image

    @app.get("/images/", response_model=List[ImageResponse])
    def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        images = db.scalars(select(Image).offset(skip).limit(limit)).all()
        return images

    @app.get("/images/{image_id}", response_model=ImageResponse)
    def read_image(image_id: str, db: Session = Depends(get_db)):
        image = db.get(Image, image_id)
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    # UserGroup endpoints
    @app.post("/user-groups/", response_model=UserGroupResponse)
    def create_user_group(user_group: UserGroupCreate, db: Session = Depends(get_db)):
        db_user_group = UserGroup(
            Id=user_group.Id,
            UserId=user_group.UserId,
            GroupId=user_group.GroupId
        )
        db.add(db_user_group)
        db.commit()
        db.refresh(db_user_group)
        return db_user_group

    @app.get("/user-groups/", response_model=List[UserGroupResponse])
    def read_user_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        user_groups = db.scalars(select(UserGroup).offset(skip).limit(limit)).all()
        return user_groups

    @app.get("/user-groups/{user_group_id}", response_model=UserGroupResponse)
    def read_user_group(user_group_id: str, db: Session = Depends(get_db)):
        user_group = db.get(UserGroup, user_group_id)
        if user_group is None:
            raise HTTPException(status_code=404, detail="UserGroup not found")
        return user_group
