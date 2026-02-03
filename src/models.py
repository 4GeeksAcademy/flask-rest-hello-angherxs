from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    PHOTO = "photo"
    VIDEO = "video"
    GIF = "gif"
    AUDIO = "audio"

class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    
    posts: Mapped[List["Post"]] = relationship(
        "Post", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    following_relationships: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    
    follower_relationships: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.followed_id",
        back_populates="followed",
        cascade="all, delete-orphan"
    )

class Follower(db.Model):
    __tablename__ = "follower"
    
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), 
        primary_key=True
    )
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), 
        primary_key=True
    )
    
    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following_relationships"
    )
    
    followed: Mapped["User"] = relationship(
        "User",
        foreign_keys=[followed_id],
        back_populates="follower_relationships"
    )

class Post(db.Model):
    __tablename__ = "post"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    user: Mapped["User"] = relationship("User", back_populates="posts")
    
    media_items: Mapped[List["Media"]] = relationship(
        "Media", 
        back_populates="post",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", 
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="Comment.created_at"
    )

class Media(db.Model):
    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    post: Mapped["Post"] = relationship("Post", back_populates="media_items")

class Comment(db.Model):
    __tablename__ = "comment"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")