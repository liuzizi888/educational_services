"""
员工信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EmployeeStatusEnum(str, Enum):
    """员工状态枚举"""
    active = "active"
    resigned = "resigned"


class EmployeeBase(BaseModel):
    """员工基础Schema"""
    user_id: Optional[int] = Field(None, description='关联用户ID')
    name: str = Field(..., min_length=1, max_length=50, description='员工姓名')
    position: Optional[str] = Field(None, max_length=100, description='职位/职能')
    phone: Optional[str] = Field(None, max_length=20, description='联系方式')
    email: Optional[str] = Field(None, max_length=100, description='邮箱')
    manager_id: Optional[int] = Field(None, description='直属上级ID')
    status: EmployeeStatusEnum = Field(EmployeeStatusEnum.active, description='在职状态')


class EmployeeCreate(EmployeeBase):
    """创建员工Schema"""
    pass


class EmployeeUpdate(BaseModel):
    """更新员工Schema"""
    user_id: Optional[int] = Field(None, description='关联用户ID')
    name: Optional[str] = Field(None, min_length=1, max_length=50, description='员工姓名')
    position: Optional[str] = Field(None, max_length=100, description='职位/职能')
    phone: Optional[str] = Field(None, max_length=20, description='联系方式')
    email: Optional[str] = Field(None, max_length=100, description='邮箱')
    manager_id: Optional[int] = Field(None, description='直属上级ID')
    status: Optional[EmployeeStatusEnum] = Field(None, description='在职状态')


class EmployeeResponse(BaseModel):
    """员工响应Schema"""
    employee_id: int
    user_id: Optional[int] = None
    name: str
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    manager_id: Optional[int] = None
    status: str
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EmployeePageResponse(BaseModel):
    """员工分页响应Schema"""
    items: list[EmployeeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
