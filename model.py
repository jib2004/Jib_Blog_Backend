from config.db import db
from sqlalchemy.orm import Mapped, mapped_column
import uuid


class User(db.Model):
    __tablename__ = 'users'
    id:Mapped[str] = mapped_column(db.String, primary_key=True,nullable=False,unique=True,default=lambda: str(uuid.uuid4()))
    email:Mapped[str] = mapped_column(db.String,nullable=False,unique=True)

    password:Mapped[str] = mapped_column(db.String,nullable=False)
    created_at:Mapped[str] = mapped_column(db.DateTime,default=db.func.now())
    updated_at:Mapped[str] = mapped_column(db.DateTime,default=db.func.now())

class Blog(db.Model):
    __tablename__ = 'blogs'
    id:Mapped[int] = mapped_column(db.Integer,primary_key=True,autoincrement=True)
    user_id:Mapped[str] = mapped_column(db.String,nullable=False,unique=True)
    title:Mapped[str] = mapped_column(db.String(250),nullable=False)
    content:Mapped[bool] = mapped_column(db.String,nullable=False,default=False)
    created_at:Mapped[str] = mapped_column(db.DateTime,default=db.func.now())
    updated_at:Mapped[str] = mapped_column(db.DateTime,default=db.func.now())
