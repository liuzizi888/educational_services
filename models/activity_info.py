"""
活动信息模型
"""
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class ActivityInfo(Base):
    """活动信息表"""
    __tablename__ = "t_activity_info"
    
    activity_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='活动名称')
    activity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='活动类型')
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='活动地点')
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='开始时间')
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='结束时间')
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='最大参与人数')
    organizer_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='负责人ID')
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='活动描述')
    status: Mapped[str] = mapped_column(String(20), default='planning', comment='活动状态')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<ActivityInfo(activity_id={self.activity_id}, activity_name={self.activity_name})>"
