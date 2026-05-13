"""
每月达成目标DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.monthly_goals import MonthlyGoals
from typing import Optional, Tuple


class MonthlyGoalsDAO:
    """每月达成目标数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> MonthlyGoals:
        """创建每月达成目标"""
        goal = MonthlyGoals(**obj_data)
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal

    @staticmethod
    def get_by_id(db: Session, goal_id: int) -> Optional[MonthlyGoals]:
        """根据ID查询每月达成目标"""
        return db.query(MonthlyGoals).filter(
            and_(
                MonthlyGoals.goal_id == goal_id,
                MonthlyGoals.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 goal_id: Optional[int] = None,
                 employee_id: Optional[int] = None,
                 status: Optional[str] = None,
                 target_month_start: Optional[str] = None,
                 target_month_end: Optional[str] = None) -> Tuple:
        """分页查询每月达成目标"""
        query = db.query(MonthlyGoals).filter(MonthlyGoals.is_deleted == 0)

        if goal_id is not None:
            query = query.filter(MonthlyGoals.goal_id == goal_id)
        if employee_id is not None:
            query = query.filter(MonthlyGoals.employee_id == employee_id)
        if status:
            query = query.filter(MonthlyGoals.status == status)
        if target_month_start:
            query = query.filter(MonthlyGoals.target_month >= target_month_start)
        if target_month_end:
            query = query.filter(MonthlyGoals.target_month <= target_month_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(MonthlyGoals.goal_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, goal_id: int, update_data: dict) -> Optional[MonthlyGoals]:
        """更新每月达成目标"""
        goal = MonthlyGoalsDAO.get_by_id(db, goal_id)
        if not goal:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(goal, key):
                setattr(goal, key, value)

        db.commit()
        db.refresh(goal)
        return goal

    @staticmethod
    def delete(db: Session, goal_id: int) -> bool:
        """删除每月达成目标（软删除）"""
        goal = MonthlyGoalsDAO.get_by_id(db, goal_id)
        if not goal:
            return False

        goal.is_deleted = 1
        db.commit()
        return True
