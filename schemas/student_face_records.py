"""
学生人脸识别Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentFaceRecordBase(BaseModel):
    """学生人脸识别基础Schema"""
    student_id: int = Field(..., description='学生ID（逻辑外键）')
    face_feature_data: Optional[str] = Field(None, description='人脸特征向量数据')
    photo_url: Optional[str] = Field(None, max_length=255, description='人脸照片存储路径')


class StudentFaceRecordCreate(StudentFaceRecordBase):
    """创建学生人脸识别Schema"""
    pass


class StudentFaceRecordUpdate(BaseModel):
    """更新学生人脸识别Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    face_feature_data: Optional[str] = Field(None, description='人脸特征向量数据')
    photo_url: Optional[str] = Field(None, max_length=255, description='人脸照片存储路径')


class StudentFaceRecordResponse(BaseModel):
    """学生人脸识别响应Schema"""
    face_id: int
    student_id: int
    face_feature_data: Optional[str] = None
    photo_url: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentFaceRecordPageResponse(BaseModel):
    """学生人脸识别分页响应Schema"""
    items: list[StudentFaceRecordResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
