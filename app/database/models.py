from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Text
from .db_session import SqlAlchemyBase
from wtforms import MultipleFileField


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    cover: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    img_content: Mapped[str] = mapped_column(nullable=True)
    video_youtube: Mapped[str] = mapped_column(nullable=True)