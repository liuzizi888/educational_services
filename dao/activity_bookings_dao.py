"""
活动预约DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.activity_bookings import ActivityBookings
from typing import Optional, Tuple


class ActivityBookingsDAO:
    """活动预约数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> ActivityBookings:
        """创建预约"""
        booking = ActivityBookings(**obj_data)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_by_id(db: Session, booking_id: int) -> Optional[ActivityBookings]:
        """根据ID查询预约"""
        return db.query(ActivityBookings).filter(
            and_(
                ActivityBookings.booking_id == booking_id,
                ActivityBookings.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 booking_id: Optional[int] = None,
                 activity_id: Optional[int] = None,
                 client_id: Optional[int] = None,
                 status: Optional[str] = None,
                 contact_name: Optional[str] = None) -> Tuple:
        """分页查询预约"""
        query = db.query(ActivityBookings).filter(ActivityBookings.is_deleted == 0)

        if booking_id is not None:
            query = query.filter(ActivityBookings.booking_id == booking_id)
        if activity_id is not None:
            query = query.filter(ActivityBookings.activity_id == activity_id)
        if client_id is not None:
            query = query.filter(ActivityBookings.client_id == client_id)
        if status:
            query = query.filter(ActivityBookings.status == status)
        if contact_name:
            query = query.filter(ActivityBookings.contact_name.like(f"%{contact_name}%"))

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(ActivityBookings.booking_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, booking_id: int, update_data: dict) -> Optional[ActivityBookings]:
        """更新预约"""
        booking = ActivityBookingsDAO.get_by_id(db, booking_id)
        if not booking:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(booking, key):
                setattr(booking, key, value)

        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def delete(db: Session, booking_id: int) -> bool:
        """删除预约（软删除）"""
        booking = ActivityBookingsDAO.get_by_id(db, booking_id)
        if not booking:
            return False

        booking.is_deleted = 1
        db.commit()
        return True
