"""
活动预约Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class BookingStatusEnum(str, Enum):
    """预约状态枚举"""
    reserved = "reserved"
    confirmed = "confirmed"
    attended = "attended"
    absent = "absent"
    cancelled = "cancelled"


class ActivityBookingBase(BaseModel):
    """预约基础Schema"""
    activity_id: Optional[int] = Field(None, description='活动ID')
    client_id: Optional[int] = Field(None, description='客户ID')
    contact_name: Optional[str] = Field(None, max_length=50, description='联系人姓名')
    contact_phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    booking_time: Optional[datetime] = Field(None, description='预约时间')
    status: BookingStatusEnum = Field(BookingStatusEnum.reserved, description='预约状态')
    remarks: Optional[str] = Field(None, description='预约备注')


class ActivityBookingCreate(ActivityBookingBase):
    """创建预约Schema"""
    pass


class ActivityBookingUpdate(BaseModel):
    """更新预约Schema"""
    activity_id: Optional[int] = Field(None, description='活动ID')
    client_id: Optional[int] = Field(None, description='客户ID')
    contact_name: Optional[str] = Field(None, max_length=50, description='联系人姓名')
    contact_phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    booking_time: Optional[datetime] = Field(None, description='预约时间')
    status: Optional[BookingStatusEnum] = Field(None, description='预约状态')
    remarks: Optional[str] = Field(None, description='预约备注')


class ActivityBookingResponse(BaseModel):
    """预约响应Schema"""
    booking_id: int
    activity_id: Optional[int] = None
    client_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    booking_time: Optional[datetime] = None
    status: str
    remarks: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ActivityBookingPageResponse(BaseModel):
    """预约分页响应Schema"""
    items: list[ActivityBookingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
