"""
用户权限模型
"""
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class UserPermissions(Base):
    """用户权限表"""
    __tablename__ = "t_user_permissions"
    
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_deleted: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=func.now())

    def __repr__(self):
        return f"<UserPermissions(user_id={self.user_id}, username={self.username}, role={self.role})>"
