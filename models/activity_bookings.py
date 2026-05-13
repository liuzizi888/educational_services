"""
活动预约模型
"""
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class ActivityBookings(Base):
    """活动预约表"""
    __tablename__ = "t_activity_bookings"
    
    booking_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='活动ID')
    client_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='客户ID')
    contact_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='联系人姓名')
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='联系电话')
    booking_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='预约时间')
    status: Mapped[str] = mapped_column(String(20), default='reserved', comment='预约状态')
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='预约备注')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<ActivityBookings(booking_id={self.booking_id}, contact_name={self.contact_name})>"
