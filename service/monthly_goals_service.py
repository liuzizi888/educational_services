"""
每月达成目标Service层
"""
from sqlalchemy.orm import Session
from dao.monthly_goals_dao import MonthlyGoalsDAO
from schemas.monthly_goals import (
    MonthlyGoalCreate,
    MonthlyGoalUpdate,
    MonthlyGoalResponse,
    MonthlyGoalPageResponse
)
from typing import Optional


class MonthlyGoalsService:
    """每月达成目标服务层"""

    @staticmethod
    def create(db: Session, obj: MonthlyGoalCreate) -> MonthlyGoalResponse:
        """创建每月达成目标"""
        obj_data = obj.model_dump()
        goal = MonthlyGoalsDAO.create(db, obj_data)
        return MonthlyGoalResponse.model_validate(goal)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 goal_id: Optional[int] = None,
                 employee_id: Optional[int] = None,
                 status: Optional[str] = None,
                 target_month_start: Optional[str] = None,
                 target_month_end: Optional[str] = None) -> MonthlyGoalPageResponse:
        """分页查询每月达成目标"""
        items, total, page, page_size, total_pages = MonthlyGoalsDAO.get_page(
            db, page, page_size, goal_id, employee_id, status, target_month_start, target_month_end
        )
        return MonthlyGoalPageResponse(
            items=[MonthlyGoalResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, goal_id: int, obj: MonthlyGoalUpdate) -> Optional[MonthlyGoalResponse]:
        """更新每月达成目标"""
        update_data = obj.model_dump(exclude_unset=True)
        goal = MonthlyGoalsDAO.update(db, goal_id, update_data)
        if goal:
            return MonthlyGoalResponse.model_validate(goal)
        return None

    @staticmethod
    def delete(db: Session, goal_id: int) -> bool:
        """删除每月达成目标"""
        return MonthlyGoalsDAO.delete(db, goal_id)
