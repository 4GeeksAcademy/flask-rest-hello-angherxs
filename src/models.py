from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey,Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    photo = "photo"
    video = "video"
    gif = "gif"
    audio = "audio"

class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

  
class Follower(db.Model):
    __tablename__="follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class Media(db.Model):
    __tablename__="media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    # type: Mapped[str] = mapped_column( nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id:Mapped[int] = mapped_column(ForeignKey("post.id"))
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

class Post(db.Model):
    __tablename__="post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

class Comment(db.Model):
    __tablename__="comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)