"""
全球留学政策模型
"""
from sqlalchemy import String, Text, Integer, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from db.database import Base


class GlobalStudyPolicies(Base):
    """全球留学政策表"""
    __tablename__ = "t_global_study_policies"
    
    policy_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False, comment='国家/地区')
    policy_category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='政策分类')
    policy_type: Mapped[str] = mapped_column(String(20), default='neutral', comment='政策倾向')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='政策标题')
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='政策内容')
    effective_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='生效日期')
    impact_level: Mapped[str] = mapped_column(String(20), default='medium', comment='影响程度')
    source_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='来源链接')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<GlobalStudyPolicies(policy_id={self.policy_id}, country={self.country}, title={self.title})>"
