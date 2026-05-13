"""
班级信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.classes import (
    ClassCreate,
    ClassUpdate,
    ClassResponse,
    ClassPageResponse
)
from service.classes_service import ClassesService
from typing import Optional

router = APIRouter(tags=["班级信息"])


@router.post("", response_model=ClassResponse)
def create(obj: ClassCreate, db: Session = Depends(get_db)):
    """创建班级信息"""
    return ClassesService.create(db, obj)


@router.get("/page", response_model=ClassPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    class_id: Optional[int] = None,
    class_name: Optional[str] = None,
    grade_level: Optional[str] = None,
    head_teacher_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询班级信息
    - class_id: 按班级ID精确查询
    - class_name: 按班级名称模糊查询
    - grade_level: 按年级筛选
    - head_teacher_id: 按班主任ID筛选
    - status: 按班级状态筛选 (active/graduated/disbanded)
    """
    return ClassesService.get_page(
        db, page, page_size, class_id, class_name, grade_level, head_teacher_id, status
    )


@router.put("/{class_id}", response_model=ClassResponse)
def update(class_id: int, obj: ClassUpdate, db: Session = Depends(get_db)):
    """更新班级信息"""
    result = ClassesService.update(db, class_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="班级信息不存在")
    return result


@router.delete("/{class_id}")
def delete(class_id: int, db: Session = Depends(get_db)):
    """删除班级信息（软删除）"""
    success = ClassesService.delete(db, class_id)
    if not success:
        raise HTTPException(status_code=404, detail="班级信息不存在")
    return {"code": 200, "msg": "删除成功"}
