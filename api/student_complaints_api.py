"""
学生投诉、建议API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.student_complaints import (
    StudentComplaintCreate,
    StudentComplaintUpdate,
    StudentComplaintResponse,
    StudentComplaintPageResponse
)
from service.student_complaints_service import StudentComplaintsService
from typing import Optional

router = APIRouter(tags=["学生投诉建议"])


@router.post("", response_model=StudentComplaintResponse)
def create(obj: StudentComplaintCreate, db: Session = Depends(get_db)):
    """创建学生投诉、建议"""
    return StudentComplaintsService.create(db, obj)


@router.get("/page", response_model=StudentComplaintPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    complaint_id: Optional[int] = None,
    student_id: Optional[int] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    handler_id: Optional[int] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生投诉、建议
    - complaint_id: 按投诉ID精确查询
    - student_id: 按学生ID筛选
    - type: 按类型筛选 (complaints/suggestions)
    - status: 按处理状态筛选 (pending/processing/resolved/rejected)
    - handler_id: 按处理人ID筛选
    - created_at_start: 按创建时间起筛选 (格式: YYYY-MM-DD HH:MM:SS)
    - created_at_end: 按创建时间止筛选 (格式: YYYY-MM-DD HH:MM:SS)
    """
    return StudentComplaintsService.get_page(
        db, page, page_size, complaint_id, student_id, type, status, handler_id, created_at_start, created_at_end
    )


@router.put("/{complaint_id}", response_model=StudentComplaintResponse)
def update(complaint_id: int, obj: StudentComplaintUpdate, db: Session = Depends(get_db)):
    """更新学生投诉、建议"""
    result = StudentComplaintsService.update(db, complaint_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生投诉、建议不存在")
    return result


@router.delete("/{complaint_id}")
def delete(complaint_id: int, db: Session = Depends(get_db)):
    """删除学生投诉、建议（软删除）"""
    success = StudentComplaintsService.delete(db, complaint_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生投诉、建议不存在")
    return {"code": 200, "msg": "删除成功"}
