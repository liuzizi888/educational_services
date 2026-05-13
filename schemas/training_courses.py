"""
培训课程Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date, time


class TrainingCourseBase(BaseModel):
    """课程基础Schema"""
    course_name: str = Field(..., min_length=1, max_length=100, description='课程名称')
    trainer_name: Optional[str] = Field(None, max_length=50, description='培训讲师')
    target_audience: Optional[str] = Field(None, max_length=100, description='培训对象')
    training_room: Optional[str] = Field(None, max_length=50, description='培训教室/线上链接')
    training_date: Optional[date] = Field(None, description='培训日期')
    start_time: Optional[time] = Field(None, description='开始时间')
    end_time: Optional[time] = Field(None, description='结束时间')
    course_content: Optional[str] = Field(None, description='课程内容')


class TrainingCourseCreate(TrainingCourseBase):
    """创建课程Schema"""
    pass


class TrainingCourseUpdate(BaseModel):
    """更新课程Schema"""
    course_name: Optional[str] = Field(None, min_length=1, max_length=100, description='课程名称')
    trainer_name: Optional[str] = Field(None, max_length=50, description='培训讲师')
    target_audience: Optional[str] = Field(None, max_length=100, description='培训对象')
    training_room: Optional[str] = Field(None, max_length=50, description='培训教室/线上链接')
    training_date: Optional[date] = Field(None, description='培训日期')
    start_time: Optional[time] = Field(None, description='开始时间')
    end_time: Optional[time] = Field(None, description='结束时间')
    course_content: Optional[str] = Field(None, description='课程内容')


class TrainingCourseResponse(BaseModel):
    """课程响应Schema"""
    course_id: int
    course_name: str
    trainer_name: Optional[str] = None
    target_audience: Optional[str] = None
    training_room: Optional[str] = None
    training_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    course_content: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TrainingCoursePageResponse(BaseModel):
    """课程分页响应Schema"""
    items: list[TrainingCourseResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
