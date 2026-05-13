"""
活动信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.activity_info import (
    ActivityInfoCreate,
    ActivityInfoUpdate,
    ActivityInfoResponse,
    ActivityInfoPageResponse
)
from service.activity_info_service import ActivityInfoService
from typing import Optional

router = APIRouter(tags=["活动管理"])


@router.post("", response_model=ActivityInfoResponse)
def create(obj: ActivityInfoCreate, db: Session = Depends(get_db)):
    """创建活动"""
    return ActivityInfoService.create(db, obj)


@router.get("/page", response_model=ActivityInfoPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    activity_id: Optional[int] = None,
    activity_name: Optional[str] = None,
    activity_type: Optional[str] = None,
    status: Optional[str] = None,
    organizer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """分页查询活动
    - activity_id: 按活动ID精确查询
    - activity_name: 按活动名称模糊查询
    - activity_type: 按活动类型筛选 (offline_saloon/online_webinar/campus_fair/training)
    - status: 按活动状态筛选 (planning/open/closed/cancelled)
    - organizer_id: 按负责人ID筛选
    """
    return ActivityInfoService.get_page(
        db, page, page_size, activity_id, activity_name, activity_type, status, organizer_id
    )


@router.get("/{activity_id}", response_model=ActivityInfoResponse)
def get_by_id(activity_id: int, db: Session = Depends(get_db)):
    """根据ID查询活动"""
    result = ActivityInfoService.get_by_id(db, activity_id)
    if not result:
        raise HTTPException(status_code=404, detail="活动不存在")
    return result


@router.put("/{activity_id}", response_model=ActivityInfoResponse)
def update(activity_id: int, obj: ActivityInfoUpdate, db: Session = Depends(get_db)):
    """更新活动"""
    result = ActivityInfoService.update(db, activity_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="活动不存在")
    return result


@router.delete("/{activity_id}")
def delete(activity_id: int, db: Session = Depends(get_db)):
    """删除活动（软删除）"""
    success = ActivityInfoService.delete(db, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="活动不存在")
    return {"code": 200, "msg": "删除成功"}
