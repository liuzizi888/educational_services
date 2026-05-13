"""
每月达成目标API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.monthly_goals import (
    MonthlyGoalCreate,
    MonthlyGoalUpdate,
    MonthlyGoalResponse,
    MonthlyGoalPageResponse
)
from service.monthly_goals_service import MonthlyGoalsService
from typing import Optional

router = APIRouter(tags=["每月达成目标"])


@router.post("", response_model=MonthlyGoalResponse)
def create(obj: MonthlyGoalCreate, db: Session = Depends(get_db)):
    """创建每月达成目标"""
    return MonthlyGoalsService.create(db, obj)


@router.get("/page", response_model=MonthlyGoalPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    goal_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    status: Optional[str] = None,
    target_month_start: Optional[str] = None,
    target_month_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询每月达成目标
    - goal_id: 按目标ID精确查询
    - employee_id: 按员工ID筛选
    - status: 按目标状态筛选 (pending/achieved/failed)
    - target_month_start: 按目标月份起筛选 (格式: YYYY-MM-DD)
    - target_month_end: 按目标月份止筛选 (格式: YYYY-MM-DD)
    """
    return MonthlyGoalsService.get_page(
        db, page, page_size, goal_id, employee_id, status, target_month_start, target_month_end
    )


@router.put("/{goal_id}", response_model=MonthlyGoalResponse)
def update(goal_id: int, obj: MonthlyGoalUpdate, db: Session = Depends(get_db)):
    """更新每月达成目标"""
    result = MonthlyGoalsService.update(db, goal_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="每月达成目标不存在")
    return result


@router.delete("/{goal_id}")
def delete(goal_id: int, db: Session = Depends(get_db)):
    """删除每月达成目标（软删除）"""
    success = MonthlyGoalsService.delete(db, goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="每月达成目标不存在")
    return {"code": 200, "msg": "删除成功"}
