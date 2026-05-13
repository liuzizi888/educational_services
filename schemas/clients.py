"""
客户信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ClientStatusEnum(str, Enum):
    """客户状态枚举"""
    new = "new"
    contacted = "contacted"
    signed = "signed"
    lost = "lost"


class ClientBase(BaseModel):
    """客户基础Schema"""
    name: Optional[str] = Field(None, max_length=100, description='客户姓名')
    phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    source: Optional[str] = Field(None, max_length=50, description='客户来源')
    status: ClientStatusEnum = Field(ClientStatusEnum.new, description='流转状态')
    assigned_employee_id: Optional[int] = Field(None, description='负责员工ID')
    notes: Optional[str] = Field(None, description='客户背景与备注')


class ClientCreate(ClientBase):
    """创建客户Schema"""
    pass


class ClientUpdate(BaseModel):
    """更新客户Schema"""
    name: Optional[str] = Field(None, max_length=100, description='客户姓名')
    phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    source: Optional[str] = Field(None, max_length=50, description='客户来源')
    status: Optional[ClientStatusEnum] = Field(None, description='流转状态')
    assigned_employee_id: Optional[int] = Field(None, description='负责员工ID')
    notes: Optional[str] = Field(None, description='客户背景与备注')


class ClientResponse(BaseModel):
    """客户响应Schema"""
    client_id: int
    name: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: str
    assigned_employee_id: Optional[int] = None
    notes: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClientPageResponse(BaseModel):
    """客户分页响应Schema"""
    items: list[ClientResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
