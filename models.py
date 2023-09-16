from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True, default=None)
