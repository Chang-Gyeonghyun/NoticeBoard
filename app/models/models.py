from sqlalchemy import Column, ForeignKey, String, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.connection import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    userID = Column(String(255), index=True, unique=True)
    password = Column(String(255))
    email = Column(String(255))
    userName = Column(String(255), index=True)
    phone = Column(String(255), index=True)
    birthday = Column(String(255),)
    address = Column(String(255))

    posts = relationship("Post", back_populates="user", lazy="joined")
    comments = relationship("Comment", back_populates="user")
    likes_dislikes = relationship("UserLikeDislike", back_populates="user", cascade="all, delete-orphan")
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    create_datetime = Column(String(255))
    last_update_datetime = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes_dislikes = relationship("UserLikeDislike", back_populates="post", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="post", cascade="all, delete-orphan")

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)

    post = relationship("Post", back_populates="attachments")
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    create_datetime = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"))
    likes = Column(Integer, default=0)   
    dislikes = Column(Integer, default=0)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", back_populates="replies", remote_side=[id])
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")
    likes_dislikes = relationship("UserLikeDislike", back_populates="comment", cascade="all, delete-orphan")

    
class UserLikeDislike(Base):
    __tablename__ = "user_likes_dislikes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    type = Column(String(10))
    
    user = relationship("User", back_populates="likes_dislikes")
    post = relationship("Post", back_populates="likes_dislikes")
    comment = relationship("Comment", back_populates="likes_dislikes")

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),
        UniqueConstraint('user_id', 'comment_id', name='_user_comment_uc'),
    )