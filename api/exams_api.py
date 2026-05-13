"""
考试信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.exams import (
    ExamCreate,
    ExamUpdate,
    ExamResponse,
    ExamPageResponse
)
from service.exams_service import ExamsService
from typing import Optional

router = APIRouter(tags=["考试信息"])


@router.post("", response_model=ExamResponse)
def create(obj: ExamCreate, db: Session = Depends(get_db)):
    """创建考试信息"""
    return ExamsService.create(db, obj)


@router.get("/page", response_model=ExamPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    exam_id: Optional[int] = None,
    class_name: Optional[str] = None,
    subject: Optional[str] = None,
    exam_name: Optional[str] = None,
    location: Optional[str] = None,
    exam_time_start: Optional[str] = None,
    exam_time_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询考试信息
    - exam_id: 按考试ID精确查询
    - class_name: 按班级名称模糊查询
    - subject: 按科目模糊查询
    - exam_name: 按考试名称模糊查询
    - location: 按考试地点模糊查询
    - exam_time_start: 按考试时间起筛选 (格式: YYYY-MM-DD HH:MM:SS)
    - exam_time_end: 按考试时间止筛选 (格式: YYYY-MM-DD HH:MM:SS)
    """
    return ExamsService.get_page(
        db, page, page_size, exam_id, class_name, subject, exam_name,
        location, exam_time_start, exam_time_end
    )


@router.put("/{exam_id}", response_model=ExamResponse)
def update(exam_id: int, obj: ExamUpdate, db: Session = Depends(get_db)):
    """更新考试信息"""
    result = ExamsService.update(db, exam_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="考试信息不存在")
    return result


@router.delete("/{exam_id}")
def delete(exam_id: int, db: Session = Depends(get_db)):
    """删除考试信息（软删除）"""
    success = ExamsService.delete(db, exam_id)
    if not success:
        raise HTTPException(status_code=404, detail="考试信息不存在")
    return {"code": 200, "msg": "删除成功"}
