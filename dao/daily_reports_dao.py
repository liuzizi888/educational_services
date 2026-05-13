"""
员工日常工作DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.daily_reports import DailyReports
from typing import Optional, Tuple


class DailyReportsDAO:
    """员工日常工作数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> DailyReports:
        """创建员工日常工作"""
        report = DailyReports(**obj_data)
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_by_id(db: Session, report_id: int) -> Optional[DailyReports]:
        """根据ID查询员工日常工作"""
        return db.query(DailyReports).filter(
            and_(
                DailyReports.report_id == report_id,
                DailyReports.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 report_id: Optional[int] = None,
                 employee_id: Optional[int] = None,
                 report_date_start: Optional[str] = None,
                 report_date_end: Optional[str] = None) -> Tuple:
        """分页查询员工日常工作"""
        query = db.query(DailyReports).filter(DailyReports.is_deleted == 0)

        if report_id is not None:
            query = query.filter(DailyReports.report_id == report_id)
        if employee_id is not None:
            query = query.filter(DailyReports.employee_id == employee_id)
        if report_date_start:
            query = query.filter(DailyReports.report_date >= report_date_start)
        if report_date_end:
            query = query.filter(DailyReports.report_date <= report_date_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(DailyReports.report_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, report_id: int, update_data: dict) -> Optional[DailyReports]:
        """更新员工日常工作"""
        report = DailyReportsDAO.get_by_id(db, report_id)
        if not report:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(report, key):
                setattr(report, key, value)

        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def delete(db: Session, report_id: int) -> bool:
        """删除员工日常工作（软删除）"""
        report = DailyReportsDAO.get_by_id(db, report_id)
        if not report:
            return False

        report.is_deleted = 1
        db.commit()
        return True
