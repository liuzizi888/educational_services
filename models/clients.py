"""
客户信息模型
"""
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class Clients(Base):
    """客户信息表"""
    __tablename__ = "t_clients"
    
    client_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='客户姓名')
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='联系电话')
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='客户来源')
    status: Mapped[str] = mapped_column(String(20), default='new', comment='流转状态')
    assigned_employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='负责员工ID')
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='客户背景与备注')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<Clients(client_id={self.client_id}, name={self.name}, status={self.status})>"
