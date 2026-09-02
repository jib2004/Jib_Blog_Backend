import datetime

from config.db import db
from sqlalchemy.orm import Mapped, mapped_column,relationship
import uuid


class User(db.Model):
    __tablename__ = 'users'
    id:Mapped[str] = mapped_column(db.String, primary_key=True,nullable=False,unique=True,default=lambda: str(uuid.uuid4()))
    email:Mapped[str] = mapped_column(db.String,nullable=False,unique=True)

    password:Mapped[str] = mapped_column(db.String,nullable=False)
    created_at:Mapped[str] = mapped_column(db.DateTime,default=db.func.now())
    updated_at:Mapped[str] = mapped_column(db.DateTime,default=db.func.now())
    blogs: Mapped[list["Blog"]] = relationship(back_populates="author")

class Blog(db.Model):
    __tablename__ = 'blogs'
    id: Mapped[int] = mapped_column(db.String, primary_key=True,nullable=False,unique=True,default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(db.String, db.ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(db.String, nullable=False)
    content: Mapped[str] = mapped_column(db.String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(db.DateTime, default=db.func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(db.DateTime, default=db.func.now())

    author: Mapped["User"] = relationship(back_populates="blogs")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author.email,   # <-- pulled via the relationship
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
