"""
学生信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class StudentBase(BaseModel):
    """学生信息基础Schema"""
    name: str = Field(..., description='学生姓名')
    gender: Optional[str] = Field(None, description='性别 M-男, F-女')
    dob: Optional[date] = Field(None, description='出生日期')
    class_id: Optional[int] = Field(None, description='所在班级ID（逻辑外键）')
    email: Optional[str] = Field(None, max_length=100, description='学生邮箱')
    parent_contact: Optional[str] = Field(None, max_length=20, description='家长联系方式')
    enrollment_date: Optional[date] = Field(None, description='入学日期')
    status: Optional[str] = Field(None, description='学籍状态: enrolled-已注册, graduated-已毕业, withdrawn-已退学')


class StudentCreate(StudentBase):
    """创建学生信息Schema"""
    pass


class StudentUpdate(BaseModel):
    """更新学生信息Schema"""
    name: Optional[str] = Field(None, description='学生姓名')
    gender: Optional[str] = Field(None, description='性别 M-男, F-女')
    dob: Optional[date] = Field(None, description='出生日期')
    class_id: Optional[int] = Field(None, description='所在班级ID（逻辑外键）')
    email: Optional[str] = Field(None, max_length=100, description='学生邮箱')
    parent_contact: Optional[str] = Field(None, max_length=20, description='家长联系方式')
    enrollment_date: Optional[date] = Field(None, description='入学日期')
    status: Optional[str] = Field(None, description='学籍状态: enrolled-已注册, graduated-已毕业, withdrawn-已退学')


class StudentResponse(BaseModel):
    """学生信息响应Schema"""
    student_id: int
    name: str
    gender: Optional[str] = None
    dob: Optional[date] = None
    class_id: Optional[int] = None
    email: Optional[str] = None
    parent_contact: Optional[str] = None
    enrollment_date: Optional[date] = None
    status: str
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentPageResponse(BaseModel):
    """学生信息分页响应Schema"""
    items: list[StudentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
