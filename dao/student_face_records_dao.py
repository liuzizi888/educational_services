"""
学生人脸识别DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.student_face_records import StudentFaceRecords
from typing import Optional, Tuple


class StudentFaceRecordsDAO:
    """学生人脸识别数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudentFaceRecords:
        """创建学生人脸识别"""
        face_record = StudentFaceRecords(**obj_data)
        db.add(face_record)
        db.commit()
        db.refresh(face_record)
        return face_record

    @staticmethod
    def get_by_id(db: Session, face_id: int) -> Optional[StudentFaceRecords]:
        """根据ID查询学生人脸识别"""
        return db.query(StudentFaceRecords).filter(
            and_(
                StudentFaceRecords.face_id == face_id,
                StudentFaceRecords.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 face_id: Optional[int] = None,
                 student_id: Optional[int] = None) -> Tuple:
        """分页查询学生人脸识别"""
        query = db.query(StudentFaceRecords).filter(StudentFaceRecords.is_deleted == 0)

        if face_id is not None:
            query = query.filter(StudentFaceRecords.face_id == face_id)
        if student_id is not None:
            query = query.filter(StudentFaceRecords.student_id == student_id)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudentFaceRecords.face_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, face_id: int, update_data: dict) -> Optional[StudentFaceRecords]:
        """更新学生人脸识别"""
        face_record = StudentFaceRecordsDAO.get_by_id(db, face_id)
        if not face_record:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(face_record, key):
                setattr(face_record, key, value)

        db.commit()
        db.refresh(face_record)
        return face_record

    @staticmethod
    def delete(db: Session, face_id: int) -> bool:
        """删除学生人脸识别（软删除）"""
        face_record = StudentFaceRecordsDAO.get_by_id(db, face_id)
        if not face_record:
            return False

        face_record.is_deleted = 1
        db.commit()
        return True
