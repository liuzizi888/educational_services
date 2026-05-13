"""
活动信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.activity_info import ActivityInfo
from typing import Optional, Tuple


class ActivityInfoDAO:
    """活动信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> ActivityInfo:
        """创建活动"""
        activity = ActivityInfo(**obj_data)
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def get_by_id(db: Session, activity_id: int) -> Optional[ActivityInfo]:
        """根据ID查询活动"""
        return db.query(ActivityInfo).filter(
            and_(
                ActivityInfo.activity_id == activity_id,
                ActivityInfo.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 activity_id: Optional[int] = None,
                 activity_name: Optional[str] = None,
                 activity_type: Optional[str] = None,
                 status: Optional[str] = None,
                 organizer_id: Optional[int] = None) -> Tuple:
        """分页查询活动"""
        query = db.query(ActivityInfo).filter(ActivityInfo.is_deleted == 0)

        if activity_id is not None:
            query = query.filter(ActivityInfo.activity_id == activity_id)
        if activity_name:
            query = query.filter(ActivityInfo.activity_name.like(f"%{activity_name}%"))
        if activity_type:
            query = query.filter(ActivityInfo.activity_type == activity_type)
        if status:
            query = query.filter(ActivityInfo.status == status)
        if organizer_id is not None:
            query = query.filter(ActivityInfo.organizer_id == organizer_id)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(ActivityInfo.activity_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, activity_id: int, update_data: dict) -> Optional[ActivityInfo]:
        """更新活动"""
        activity = ActivityInfoDAO.get_by_id(db, activity_id)
        if not activity:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(activity, key):
                setattr(activity, key, value)

        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def delete(db: Session, activity_id: int) -> bool:
        """删除活动（软删除）"""
        activity = ActivityInfoDAO.get_by_id(db, activity_id)
        if not activity:
            return False

        activity.is_deleted = 1
        db.commit()
        return True
