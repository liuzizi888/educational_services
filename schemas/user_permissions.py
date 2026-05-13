"""
用户权限Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    """用户角色枚举"""
    admin = "admin"
    employee = "employee"
    student = "student"
    teacher = "teacher"


class UserPermissionsBase(BaseModel):
    """用户权限基础Schema"""
    username: str = Field(..., min_length=1, max_length=50, description="登录账号")
    role: RoleEnum = Field(..., description="角色：admin、employee、student、teacher")


class UserPermissionsCreate(UserPermissionsBase):
    """创建用户Schema"""
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserPermissionsUpdate(BaseModel):
    """更新用户Schema"""
    username: Optional[str] = Field(None, min_length=1, max_length=50, description="登录账号")
    password: Optional[str] = Field(None, min_length=6, max_length=50, description="密码")
    role: Optional[RoleEnum] = Field(None, description="角色")


class UserPermissionsResponse(BaseModel):
    """用户响应Schema"""
    user_id: int
    username: str
    role: str
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPermissionsPageResponse(BaseModel):
    """用户分页响应Schema"""
    items: list[UserPermissionsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class LoginRequest(BaseModel):
    """登录请求Schema"""
    username: str = Field(..., min_length=1, max_length=50, description="登录账号")
    password: str = Field(..., min_length=1, description="密码")


class LoginResponse(BaseModel):
    """登录响应Schema"""
    code: int = Field(200, description="状态码")
    msg: str = Field("登录成功", description="消息")
    token: str = Field(..., description="访问令牌")
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    role: str = Field(..., description="角色")
