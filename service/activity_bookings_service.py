"""
活动预约Service层
"""
from sqlalchemy.orm import Session
from dao.activity_bookings_dao import ActivityBookingsDAO
from schemas.activity_bookings import (
    ActivityBookingCreate,
    ActivityBookingUpdate,
    ActivityBookingResponse,
    ActivityBookingPageResponse
)
from typing import Optional


class ActivityBookingsService:
    """活动预约服务层"""

    @staticmethod
    def create(db: Session, obj: ActivityBookingCreate) -> ActivityBookingResponse:
        """创建预约"""
        obj_data = obj.model_dump()
        booking = ActivityBookingsDAO.create(db, obj_data)
        return ActivityBookingResponse.model_validate(booking)

    @staticmethod
    def get_by_id(db: Session, booking_id: int) -> Optional[ActivityBookingResponse]:
        """根据ID查询预约"""
        booking = ActivityBookingsDAO.get_by_id(db, booking_id)
        if booking:
            return ActivityBookingResponse.model_validate(booking)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 booking_id: Optional[int] = None,
                 activity_id: Optional[int] = None,
                 client_id: Optional[int] = None,
                 status: Optional[str] = None,
                 contact_name: Optional[str] = None) -> ActivityBookingPageResponse:
        """分页查询预约"""
        items, total, page, page_size, total_pages = ActivityBookingsDAO.get_page(
            db, page, page_size, booking_id, activity_id, client_id, status, contact_name
        )
        return ActivityBookingPageResponse(
            items=[ActivityBookingResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, booking_id: int, obj: ActivityBookingUpdate) -> Optional[ActivityBookingResponse]:
        """更新预约"""
        update_data = obj.model_dump(exclude_unset=True)
        booking = ActivityBookingsDAO.update(db, booking_id, update_data)
        if booking:
            return ActivityBookingResponse.model_validate(booking)
        return None

    @staticmethod
    def delete(db: Session, booking_id: int) -> bool:
        """删除预约"""
        return ActivityBookingsDAO.delete(db, booking_id)
