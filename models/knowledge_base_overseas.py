"""
海外生活知识库模型
"""
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class KnowledgeBaseOverseas(Base):
    """海外生活常识与指南知识库"""
    __tablename__ = "t_knowledge_base_overseas"

    kb_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='知识ID')
    country: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='国家（如：英国、美国）')
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='分类（如：安全、交通、医疗）')
    question: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='标准问题')
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='详细回答')
    keywords: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='关键词标签，用于检索')
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='最后更新人ID（逻辑外键）')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<KnowledgeBaseOverseas(kb_id={self.kb_id}, country={self.country}, category={self.category})>"
