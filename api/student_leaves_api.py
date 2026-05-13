"""
学生请假API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.student_leaves import (
    StudentLeaveCreate,
    StudentLeaveUpdate,
    StudentLeaveResponse,
    StudentLeavePageResponse
)
from service.student_leaves_service import StudentLeavesService
from typing import Optional

router = APIRouter(tags=["学生请假"])


@router.post("", response_model=StudentLeaveResponse)
def create(obj: StudentLeaveCreate, db: Session = Depends(get_db)):
    """创建学生请假"""
    return StudentLeavesService.create(db, obj)


@router.get("/page", response_model=StudentLeavePageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    leave_id: Optional[int] = None,
    student_id: Optional[int] = None,
    approver_id: Optional[int] = None,
    status: Optional[str] = None,
    start_time_start: Optional[str] = None,
    start_time_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生请假
    - leave_id: 按请假ID精确查询
    - student_id: 按学生ID筛选
    - approver_id: 按审批人ID筛选
    - status: 按审批状态筛选 (pending/approved/rejected)
    - start_time_start: 按请假开始时间起筛选 (格式: YYYY-MM-DD HH:MM:SS)
    - start_time_end: 按请假开始时间止筛选 (格式: YYYY-MM-DD HH:MM:SS)
    """
    return StudentLeavesService.get_page(
        db, page, page_size, leave_id, student_id, approver_id, status, start_time_start, start_time_end
    )


@router.put("/{leave_id}", response_model=StudentLeaveResponse)
def update(leave_id: int, obj: StudentLeaveUpdate, db: Session = Depends(get_db)):
    """更新学生请假"""
    result = StudentLeavesService.update(db, leave_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生请假不存在")
    return result


@router.delete("/{leave_id}")
def delete(leave_id: int, db: Session = Depends(get_db)):
    """删除学生请假（软删除）"""
    success = StudentLeavesService.delete(db, leave_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生请假不存在")
    return {"code": 200, "msg": "删除成功"}
