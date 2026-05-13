"""
班级信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ClassBase(BaseModel):
    """班级信息基础Schema"""
    class_name: str = Field(..., description='班级名称')
    grade_level: Optional[str] = Field(None, max_length=50, description='年级')
    head_teacher_id: Optional[int] = Field(None, description='班主任ID（逻辑外键）')
    classroom_location: Optional[str] = Field(None, max_length=100, description='固定教室/地点')
    max_students: Optional[int] = Field(None, ge=0, description='班级最大人数')
    current_students: Optional[int] = Field(None, ge=0, description='当前在读人数')
    status: Optional[str] = Field(None, description='班级状态: active-在读, graduated-已毕业, disbanded-已解散')


class ClassCreate(ClassBase):
    """创建班级信息Schema"""
    pass


class ClassUpdate(BaseModel):
    """更新班级信息Schema"""
    class_name: Optional[str] = Field(None, description='班级名称')
    grade_level: Optional[str] = Field(None, max_length=50, description='年级')
    head_teacher_id: Optional[int] = Field(None, description='班主任ID（逻辑外键）')
    classroom_location: Optional[str] = Field(None, max_length=100, description='固定教室/地点')
    max_students: Optional[int] = Field(None, ge=0, description='班级最大人数')
    current_students: Optional[int] = Field(None, ge=0, description='当前在读人数')
    status: Optional[str] = Field(None, description='班级状态: active-在读, graduated-已毕业, disbanded-已解散')


class ClassResponse(BaseModel):
    """班级信息响应Schema"""
    class_id: int
    class_name: str
    grade_level: Optional[str] = None
    head_teacher_id: Optional[int] = None
    classroom_location: Optional[str] = None
    max_students: Optional[int] = None
    current_students: int
    status: str
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClassPageResponse(BaseModel):
    """班级信息分页响应Schema"""
    items: list[ClassResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
