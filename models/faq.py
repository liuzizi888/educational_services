"""
常见问题模型
"""
from sqlalchemy import String, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class Faq(Base):
    """常见问题表"""
    __tablename__ = "t_faq"
    
    faq_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='问题分类')
    question: Mapped[str] = mapped_column(String(255), nullable=False, comment='问题')
    answer: Mapped[str] = mapped_column(Text, nullable=False, comment='回答')
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment='排序权重')
    view_count: Mapped[int] = mapped_column(Integer, default=0, comment='查看次数')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment='是否启用')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<Faq(faq_id={self.faq_id}, question={self.question})>"
