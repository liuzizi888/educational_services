"""
学生成绩DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.student_grades import StudentGrades
from typing import Optional, Tuple


class StudentGradesDAO:
    """学生成绩数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudentGrades:
        """创建学生成绩"""
        grade = StudentGrades(**obj_data)
        db.add(grade)
        db.commit()
        db.refresh(grade)
        return grade

    @staticmethod
    def get_by_id(db: Session, grade_id: int) -> Optional[StudentGrades]:
        """根据ID查询学生成绩"""
        return db.query(StudentGrades).filter(
            and_(
                StudentGrades.grade_id == grade_id,
                StudentGrades.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 grade_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 subject: Optional[str] = None,
                 exam_type: Optional[str] = None,
                 score_min: Optional[float] = None,
                 score_max: Optional[float] = None,
                 exam_date_start: Optional[str] = None,
                 exam_date_end: Optional[str] = None) -> Tuple:
        """分页查询学生成绩"""
        query = db.query(StudentGrades).filter(StudentGrades.is_deleted == 0)

        if grade_id is not None:
            query = query.filter(StudentGrades.grade_id == grade_id)
        if student_id is not None:
            query = query.filter(StudentGrades.student_id == student_id)
        if subject:
            query = query.filter(StudentGrades.subject.like(f"%{subject}%"))
        if exam_type:
            query = query.filter(StudentGrades.exam_type.like(f"%{exam_type}%"))
        if score_min is not None:
            query = query.filter(StudentGrades.score >= score_min)
        if score_max is not None:
            query = query.filter(StudentGrades.score <= score_max)
        if exam_date_start:
            query = query.filter(StudentGrades.exam_date >= exam_date_start)
        if exam_date_end:
            query = query.filter(StudentGrades.exam_date <= exam_date_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudentGrades.grade_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, grade_id: int, update_data: dict) -> Optional[StudentGrades]:
        """更新学生成绩"""
        grade = StudentGradesDAO.get_by_id(db, grade_id)
        if not grade:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(grade, key):
                setattr(grade, key, value)

        db.commit()
        db.refresh(grade)
        return grade

    @staticmethod
    def delete(db: Session, grade_id: int) -> bool:
        """删除学生成绩（软删除）"""
        grade = StudentGradesDAO.get_by_id(db, grade_id)
        if not grade:
            return False

        grade.is_deleted = 1
        db.commit()
        return True
