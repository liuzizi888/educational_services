"""
学生成绩API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.student_grades import (
    StudentGradeCreate,
    StudentGradeUpdate,
    StudentGradeResponse,
    StudentGradePageResponse
)
from service.student_grades_service import StudentGradesService
from typing import Optional

router = APIRouter(tags=["学生成绩"])


@router.post("", response_model=StudentGradeResponse)
def create(obj: StudentGradeCreate, db: Session = Depends(get_db)):
    """创建学生成绩"""
    return StudentGradesService.create(db, obj)


@router.get("/page", response_model=StudentGradePageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    grade_id: Optional[int] = None,
    student_id: Optional[int] = None,
    subject: Optional[str] = None,
    exam_type: Optional[str] = None,
    score_min: Optional[float] = None,
    score_max: Optional[float] = None,
    exam_date_start: Optional[str] = None,
    exam_date_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生成绩
    - grade_id: 按成绩ID精确查询
    - student_id: 按学生ID筛选
    - subject: 按科目模糊查询
    - exam_type: 按考试类型模糊查询
    - score_min: 按分数最小值筛选
    - score_max: 按分数最大值筛选
    - exam_date_start: 按考试日期起筛选 (格式: YYYY-MM-DD)
    - exam_date_end: 按考试日期止筛选 (格式: YYYY-MM-DD)
    """
    return StudentGradesService.get_page(
        db, page, page_size, grade_id, student_id, subject, exam_type,
        score_min, score_max, exam_date_start, exam_date_end
    )


@router.put("/{grade_id}", response_model=StudentGradeResponse)
def update(grade_id: int, obj: StudentGradeUpdate, db: Session = Depends(get_db)):
    """更新学生成绩"""
    result = StudentGradesService.update(db, grade_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生成绩不存在")
    return result


@router.delete("/{grade_id}")
def delete(grade_id: int, db: Session = Depends(get_db)):
    """删除学生成绩（软删除）"""
    success = StudentGradesService.delete(db, grade_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生成绩不存在")
    return {"code": 200, "msg": "删除成功"}
