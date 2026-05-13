"""
学生成绩Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class StudentGradeBase(BaseModel):
    """学生成绩基础Schema"""
    student_id: int = Field(..., description='学生ID（逻辑外键）')
    subject: Optional[str] = Field(None, max_length=100, description='科目')
    score: Optional[float] = Field(None, ge=0, le=100, description='分数')
    exam_type: Optional[str] = Field(None, max_length=50, description='考试类型（期中考、期末考等）')
    exam_date: Optional[date] = Field(None, description='考试日期')
    teacher_remark: Optional[str] = Field(None, max_length=255, description='教师评语')


class StudentGradeCreate(StudentGradeBase):
    """创建学生成绩Schema"""
    pass


class StudentGradeUpdate(BaseModel):
    """更新学生成绩Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    subject: Optional[str] = Field(None, max_length=100, description='科目')
    score: Optional[float] = Field(None, ge=0, le=100, description='分数')
    exam_type: Optional[str] = Field(None, max_length=50, description='考试类型（期中考、期末考等）')
    exam_date: Optional[date] = Field(None, description='考试日期')
    teacher_remark: Optional[str] = Field(None, max_length=255, description='教师评语')


class StudentGradeResponse(BaseModel):
    """学生成绩响应Schema"""
    grade_id: int
    student_id: int
    subject: Optional[str] = None
    score: Optional[float] = None
    exam_type: Optional[str] = None
    exam_date: Optional[date] = None
    teacher_remark: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentGradePageResponse(BaseModel):
    """学生成绩分页响应Schema"""
    items: list[StudentGradeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
