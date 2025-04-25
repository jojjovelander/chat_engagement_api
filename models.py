# models.py
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Text, ForeignKey, Select
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Group(Base):
    __tablename__ = "Groups"
    Id = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Assistant = Column(String, nullable=False)
    Active = Column(Boolean, nullable=False)

    threads = relationship("Thread", back_populates="group")
    user_groups = relationship("UserGroup", back_populates="group")


class Role(Base):
    __tablename__ = "Roles"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "Users"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    UserId = Column(String, nullable=False)
    LoginToken = Column(Integer)
    Email = Column(String, nullable=False)
    RoleId = Column(Integer, ForeignKey("Roles.Id", ondelete="CASCADE"), nullable=False)
    CreatedUtc = Column(String, nullable=False, default='-infinity')
    LastAccessedUtc = Column(String, nullable=False, default='-infinity')

    role = relationship("Role", back_populates="users")
    threads = relationship("Thread", back_populates="user")
    user_groups = relationship("UserGroup", back_populates="user")


class Thread(Base):
    __tablename__ = "Threads"
    Id = Column(String, primary_key=True)
    UserId = Column(Integer, ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    Created = Column(String, nullable=False)
    Title = Column(String, nullable=False, default="")
    GroupId = Column(String, ForeignKey("Groups.Id"))

    user = relationship("User", back_populates="threads")
    group = relationship("Group", back_populates="threads")
    images = relationship("Image", back_populates="thread")
    messages = relationship("Message", back_populates="thread")


class Image(Base):
    __tablename__ = "Images"
    Id = Column(String, primary_key=True)
    ThreadId = Column(String, ForeignKey("Threads.Id", ondelete="CASCADE"), nullable=False)
    Data = Column(Text, nullable=False)

    thread = relationship("Thread", back_populates="images")


class Message(Base):
    __tablename__ = "Messages"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ThreadId = Column(String, ForeignKey("Threads.Id", ondelete="CASCADE"), nullable=False)
    Text = Column(Text, nullable=False)
    Created = Column(String, nullable=False)
    Role = Column(Integer, nullable=False)

    thread = relationship("Thread", back_populates="messages")


class UserGroup(Base):
    __tablename__ = "UserGroups"
    Id = Column(String, primary_key=True)
    UserId = Column(Integer, ForeignKey("Users.Id", ondelete="RESTRICT"))
    GroupId = Column(String, ForeignKey("Groups.Id", ondelete="RESTRICT"))

    user = relationship("User", back_populates="user_groups")
    group = relationship("Group", back_populates="user_groups")