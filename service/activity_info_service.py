"""
活动信息Service层
"""
from sqlalchemy.orm import Session
from dao.activity_info_dao import ActivityInfoDAO
from schemas.activity_info import (
    ActivityInfoCreate,
    ActivityInfoUpdate,
    ActivityInfoResponse,
    ActivityInfoPageResponse
)
from typing import Optional


class ActivityInfoService:
    """活动信息服务层"""

    @staticmethod
    def create(db: Session, obj: ActivityInfoCreate) -> ActivityInfoResponse:
        """创建活动"""
        obj_data = obj.model_dump()
        activity = ActivityInfoDAO.create(db, obj_data)
        return ActivityInfoResponse.model_validate(activity)

    @staticmethod
    def get_by_id(db: Session, activity_id: int) -> Optional[ActivityInfoResponse]:
        """根据ID查询活动"""
        activity = ActivityInfoDAO.get_by_id(db, activity_id)
        if activity:
            return ActivityInfoResponse.model_validate(activity)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 activity_id: Optional[int] = None,
                 activity_name: Optional[str] = None,
                 activity_type: Optional[str] = None,
                 status: Optional[str] = None,
                 organizer_id: Optional[int] = None) -> ActivityInfoPageResponse:
        """分页查询活动"""
        items, total, page, page_size, total_pages = ActivityInfoDAO.get_page(
            db, page, page_size, activity_id, activity_name, activity_type, status, organizer_id
        )
        return ActivityInfoPageResponse(
            items=[ActivityInfoResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, activity_id: int, obj: ActivityInfoUpdate) -> Optional[ActivityInfoResponse]:
        """更新活动"""
        update_data = obj.model_dump(exclude_unset=True)
        activity = ActivityInfoDAO.update(db, activity_id, update_data)
        if activity:
            return ActivityInfoResponse.model_validate(activity)
        return None

    @staticmethod
    def delete(db: Session, activity_id: int) -> bool:
        """删除活动"""
        return ActivityInfoDAO.delete(db, activity_id)
