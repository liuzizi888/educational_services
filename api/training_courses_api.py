"""
培训课程API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.training_courses import (
    TrainingCourseCreate,
    TrainingCourseUpdate,
    TrainingCourseResponse,
    TrainingCoursePageResponse
)
from service.training_courses_service import TrainingCoursesService
from typing import Optional

router = APIRouter(tags=["培训课程"])


@router.post("", response_model=TrainingCourseResponse)
def create(obj: TrainingCourseCreate, db: Session = Depends(get_db)):
    """创建培训课程"""
    return TrainingCoursesService.create(db, obj)


@router.get("/page", response_model=TrainingCoursePageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    course_id: Optional[int] = None,
    course_name: Optional[str] = None,
    trainer_name: Optional[str] = None,
    training_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询培训课程
    - course_id: 按课程ID精确查询
    - course_name: 按课程名称模糊查询
    - trainer_name: 按讲师姓名模糊查询
    - training_date: 按培训日期筛选 (格式: YYYY-MM-DD)
    """
    return TrainingCoursesService.get_page(
        db, page, page_size, course_id, course_name, trainer_name, training_date
    )


@router.get("/{course_id}", response_model=TrainingCourseResponse)
def get_by_id(course_id: int, db: Session = Depends(get_db)):
    """根据ID查询培训课程"""
    result = TrainingCoursesService.get_by_id(db, course_id)
    if not result:
        raise HTTPException(status_code=404, detail="课程不存在")
    return result


@router.put("/{course_id}", response_model=TrainingCourseResponse)
def update(course_id: int, obj: TrainingCourseUpdate, db: Session = Depends(get_db)):
    """更新培训课程"""
    result = TrainingCoursesService.update(db, course_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="课程不存在")
    return result


@router.delete("/{course_id}")
def delete(course_id: int, db: Session = Depends(get_db)):
    """删除培训课程（软删除）"""
    success = TrainingCoursesService.delete(db, course_id)
    if not success:
        raise HTTPException(status_code=404, detail="课程不存在")
    return {"code": 200, "msg": "删除成功"}
