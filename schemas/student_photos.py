"""
学生人脸识别与心情预判Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PhotoRiskLevelEnum(str, Enum):
    green = "green"
    yellow = "yellow"
    orange = "orange"
    red = "red"


class StudentPhotoBase(BaseModel):
    """学生人脸识别与心情预判基础Schema"""
    student_id: int = Field(..., description='学生ID（逻辑关联）')
    photo_url: Optional[str] = Field(None, max_length=255, description='抓拍照片存储路径')
    mood_status: Optional[str] = Field(None, max_length=20, description='识别出的心情状态（开心、平静、焦虑、愤怒、悲伤）')
    risk_level: Optional[str] = Field('green', description='风险等级: green-绿色, yellow-黄色, orange-橙色, red-红色')
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description='情绪评分 (-1.0 到 1.0)')
    capture_scene: Optional[str] = Field(None, max_length=50, description='抓拍场景（校门闸机、宿舍门口、教室摄像头）')
    device_id: Optional[str] = Field(None, max_length=50, description='抓拍设备编号')


class StudentPhotoCreate(StudentPhotoBase):
    """创建学生人脸识别记录Schema"""
    pass


class StudentPhotoUpdate(BaseModel):
    """更新学生人脸识别记录Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑关联）')
    photo_url: Optional[str] = Field(None, max_length=255, description='抓拍照片存储路径')
    mood_status: Optional[str] = Field(None, max_length=20, description='识别出的心情状态（开心、平静、焦虑、愤怒、悲伤）')
    risk_level: Optional[str] = Field(None, description='风险等级: green-绿色, yellow-黄色, orange-橙色, red-红色')
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description='情绪评分 (-1.0 到 1.0)')
    capture_scene: Optional[str] = Field(None, max_length=50, description='抓拍场景（校门闸机、宿舍门口、教室摄像头）')
    device_id: Optional[str] = Field(None, max_length=50, description='抓拍设备编号')


class StudentPhotoResponse(BaseModel):
    """学生人脸识别记录响应Schema"""
    photo_id: int
    student_id: int
    photo_url: Optional[str] = None
    mood_status: Optional[str] = None
    risk_level: str
    sentiment_score: Optional[float] = None
    capture_scene: Optional[str] = None
    device_id: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentPhotoPageResponse(BaseModel):
    """学生人脸识别记录分页响应Schema"""
    items: list[StudentPhotoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
