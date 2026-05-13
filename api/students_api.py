"""
学生信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.students import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentPageResponse
)
from service.students_service import StudentsService
from typing import Optional

router = APIRouter(tags=["学生信息"])


@router.post("", response_model=StudentResponse)
def create(obj: StudentCreate, db: Session = Depends(get_db)):
    """创建学生信息"""
    return StudentsService.create(db, obj)


@router.get("/page", response_model=StudentPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    student_id: Optional[int] = None,
    class_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    enrollment_date_start: Optional[str] = None,
    enrollment_date_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生信息
    - student_id: 按学生ID精确查询
    - class_id: 按班级ID筛选
    - name: 按学生姓名模糊查询
    - status: 按学籍状态筛选 (enrolled/graduated/withdrawn)
    - enrollment_date_start: 按入学日期起筛选 (格式: YYYY-MM-DD)
    - enrollment_date_end: 按入学日期止筛选 (格式: YYYY-MM-DD)
    """
    return StudentsService.get_page(
        db, page, page_size, student_id, class_id, name, status, enrollment_date_start, enrollment_date_end
    )


@router.put("/{student_id}", response_model=StudentResponse)
def update(student_id: int, obj: StudentUpdate, db: Session = Depends(get_db)):
    """更新学生信息"""
    result = StudentsService.update(db, student_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生信息不存在")
    return result


@router.delete("/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    """删除学生信息（软删除）"""
    success = StudentsService.delete(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生信息不存在")
    return {"code": 200, "msg": "删除成功"}
