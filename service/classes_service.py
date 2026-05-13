"""
班级信息Service层
"""
from sqlalchemy.orm import Session
from dao.classes_dao import ClassesDAO
from schemas.classes import (
    ClassCreate,
    ClassUpdate,
    ClassResponse,
    ClassPageResponse
)
from typing import Optional


class ClassesService:
    """班级信息服务层"""

    @staticmethod
    def create(db: Session, obj: ClassCreate) -> ClassResponse:
        """创建班级信息"""
        obj_data = obj.model_dump()
        class_obj = ClassesDAO.create(db, obj_data)
        return ClassResponse.model_validate(class_obj)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 class_id: Optional[int] = None,
                 class_name: Optional[str] = None,
                 grade_level: Optional[str] = None,
                 head_teacher_id: Optional[int] = None,
                 status: Optional[str] = None) -> ClassPageResponse:
        """分页查询班级信息"""
        items, total, page, page_size, total_pages = ClassesDAO.get_page(
            db, page, page_size, class_id, class_name, grade_level, head_teacher_id, status
        )
        return ClassPageResponse(
            items=[ClassResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, class_id: int, obj: ClassUpdate) -> Optional[ClassResponse]:
        """更新班级信息"""
        update_data = obj.model_dump(exclude_unset=True)
        class_obj = ClassesDAO.update(db, class_id, update_data)
        if class_obj:
            return ClassResponse.model_validate(class_obj)
        return None

    @staticmethod
    def delete(db: Session, class_id: int) -> bool:
        """删除班级信息"""
        return ClassesDAO.delete(db, class_id)
