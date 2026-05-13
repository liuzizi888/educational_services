"""
学生人脸识别Service层
"""
from sqlalchemy.orm import Session
from dao.student_face_records_dao import StudentFaceRecordsDAO
from schemas.student_face_records import (
    StudentFaceRecordCreate,
    StudentFaceRecordUpdate,
    StudentFaceRecordResponse,
    StudentFaceRecordPageResponse
)
from typing import Optional


class StudentFaceRecordsService:
    """学生人脸识别服务层"""

    @staticmethod
    def create(db: Session, obj: StudentFaceRecordCreate) -> StudentFaceRecordResponse:
        """创建学生人脸识别"""
        obj_data = obj.model_dump()
        face_record = StudentFaceRecordsDAO.create(db, obj_data)
        return StudentFaceRecordResponse.model_validate(face_record)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 face_id: Optional[int] = None,
                 student_id: Optional[int] = None) -> StudentFaceRecordPageResponse:
        """分页查询学生人脸识别"""
        items, total, page, page_size, total_pages = StudentFaceRecordsDAO.get_page(
            db, page, page_size, face_id, student_id
        )
        return StudentFaceRecordPageResponse(
            items=[StudentFaceRecordResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, face_id: int, obj: StudentFaceRecordUpdate) -> Optional[StudentFaceRecordResponse]:
        """更新学生人脸识别"""
        update_data = obj.model_dump(exclude_unset=True)
        face_record = StudentFaceRecordsDAO.update(db, face_id, update_data)
        if face_record:
            return StudentFaceRecordResponse.model_validate(face_record)
        return None

    @staticmethod
    def delete(db: Session, face_id: int) -> bool:
        """删除学生人脸识别"""
        return StudentFaceRecordsDAO.delete(db, face_id)
