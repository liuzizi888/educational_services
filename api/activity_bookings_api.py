"""
活动预约API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.activity_bookings import (
    ActivityBookingCreate,
    ActivityBookingUpdate,
    ActivityBookingResponse,
    ActivityBookingPageResponse
)
from service.activity_bookings_service import ActivityBookingsService
from typing import Optional

router = APIRouter(tags=["活动预约"])


@router.post("", response_model=ActivityBookingResponse)
def create(obj: ActivityBookingCreate, db: Session = Depends(get_db)):
    """创建活动预约"""
    return ActivityBookingsService.create(db, obj)


@router.get("/page", response_model=ActivityBookingPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    booking_id: Optional[int] = None,
    activity_id: Optional[int] = None,
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    contact_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询活动预约
    - booking_id: 按预约ID精确查询
    - activity_id: 按活动ID筛选
    - client_id: 按客户ID筛选
    - status: 按预约状态筛选 (reserved/confirmed/attended/absent/cancelled)
    - contact_name: 按联系人姓名模糊查询
    """
    return ActivityBookingsService.get_page(
        db, page, page_size, booking_id, activity_id, client_id, status, contact_name
    )


@router.get("/{booking_id}", response_model=ActivityBookingResponse)
def get_by_id(booking_id: int, db: Session = Depends(get_db)):
    """根据ID查询活动预约"""
    result = ActivityBookingsService.get_by_id(db, booking_id)
    if not result:
        raise HTTPException(status_code=404, detail="预约不存在")
    return result


@router.put("/{booking_id}", response_model=ActivityBookingResponse)
def update(booking_id: int, obj: ActivityBookingUpdate, db: Session = Depends(get_db)):
    """更新活动预约"""
    result = ActivityBookingsService.update(db, booking_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="预约不存在")
    return result


@router.delete("/{booking_id}")
def delete(booking_id: int, db: Session = Depends(get_db)):
    """删除活动预约（软删除）"""
    success = ActivityBookingsService.delete(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="预约不存在")
    return {"code": 200, "msg": "删除成功"}
