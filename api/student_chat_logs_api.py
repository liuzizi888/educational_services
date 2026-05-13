"""
学生聊天记录API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.student_chat_logs import (
    StudentChatLogCreate,
    StudentChatLogUpdate,
    StudentChatLogResponse,
    StudentChatLogPageResponse
)
from service.student_chat_logs_service import StudentChatLogsService
from typing import Optional

router = APIRouter(tags=["学生聊天记录"])


@router.post("", response_model=StudentChatLogResponse)
def create(obj: StudentChatLogCreate, db: Session = Depends(get_db)):
    """创建学生聊天记录"""
    return StudentChatLogsService.create(db, obj)


@router.get("/page", response_model=StudentChatLogPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    log_id: Optional[int] = None,
    student_id: Optional[int] = None,
    risk_level: Optional[str] = None,
    keywords: Optional[str] = None,
    sentiment_min: Optional[float] = None,
    sentiment_max: Optional[float] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生聊天记录
    - log_id: 按日志ID精确查询
    - student_id: 按学生ID筛选
    - risk_level: 按风险等级筛选 (green/yellow/orange/red)
    - keywords: 按敏感词模糊查询
    - sentiment_min: 按情绪评分最小值筛选
    - sentiment_max: 按情绪评分最大值筛选
    - created_at_start: 按聊天时间起筛选 (格式: YYYY-MM-DD HH:MM:SS)
    - created_at_end: 按聊天时间止筛选 (格式: YYYY-MM-DD HH:MM:SS)
    """
    return StudentChatLogsService.get_page(
        db, page, page_size, log_id, student_id, risk_level, keywords,
        sentiment_min, sentiment_max, created_at_start, created_at_end
    )


@router.put("/{log_id}", response_model=StudentChatLogResponse)
def update(log_id: int, obj: StudentChatLogUpdate, db: Session = Depends(get_db)):
    """更新学生聊天记录"""
    result = StudentChatLogsService.update(db, log_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生聊天记录不存在")
    return result


@router.delete("/{log_id}")
def delete(log_id: int, db: Session = Depends(get_db)):
    """删除学生聊天记录（软删除）"""
    success = StudentChatLogsService.delete(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生聊天记录不存在")
    return {"code": 200, "msg": "删除成功"}
