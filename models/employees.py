"""
员工信息模型
"""
from sqlalchemy import String, Integer, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class Employees(Base):
    """员工信息表"""
    __tablename__ = "t_employees"
    
    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='关联用户ID')
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='员工姓名')
    position: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='职位/职能')
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='联系方式')
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='邮箱')
    manager_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='直属上级ID')
    status: Mapped[str] = mapped_column(String(20), default='active', comment='在职状态')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=func.now())

    def __repr__(self):
        return f"<Employees(employee_id={self.employee_id}, name={self.name}, position={self.position})>"
