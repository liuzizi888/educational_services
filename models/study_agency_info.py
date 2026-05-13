"""
留学机构合作信息模型
"""
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class StudyAgencyInfo(Base):
    """留学机构合作信息表"""
    __tablename__ = "t_study_agency_info"
    
    agency_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agency_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='机构名称')
    country: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='所属国家')
    contact_person: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='联系人')
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='联系电话')
    contact_email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='联系邮箱')
    cooperation_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='合作类型')
    cooperation_status: Mapped[str] = mapped_column(String(20), default='active', comment='合作状态')
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='合作备注')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudyAgencyInfo(agency_id={self.agency_id}, agency_name={self.agency_name})>"
