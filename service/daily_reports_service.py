"""
员工日常工作Service层
"""
from sqlalchemy.orm import Session
from dao.daily_reports_dao import DailyReportsDAO
from schemas.daily_reports import (
    DailyReportCreate,
    DailyReportUpdate,
    DailyReportResponse,
    DailyReportPageResponse
)
from typing import Optional


class DailyReportsService:
    """员工日常工作服务层"""

    @staticmethod
    def create(db: Session, obj: DailyReportCreate) -> DailyReportResponse:
        """创建员工日常工作"""
        obj_data = obj.model_dump()
        report = DailyReportsDAO.create(db, obj_data)
        return DailyReportResponse.model_validate(report)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 report_id: Optional[int] = None,
                 employee_id: Optional[int] = None,
                 report_date_start: Optional[str] = None,
                 report_date_end: Optional[str] = None) -> DailyReportPageResponse:
        """分页查询员工日常工作"""
        items, total, page, page_size, total_pages = DailyReportsDAO.get_page(
            db, page, page_size, report_id, employee_id, report_date_start, report_date_end
        )
        return DailyReportPageResponse(
            items=[DailyReportResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, report_id: int, obj: DailyReportUpdate) -> Optional[DailyReportResponse]:
        """更新员工日常工作"""
        update_data = obj.model_dump(exclude_unset=True)
        report = DailyReportsDAO.update(db, report_id, update_data)
        if report:
            return DailyReportResponse.model_validate(report)
        return None

    @staticmethod
    def delete(db: Session, report_id: int) -> bool:
        """删除员工日常工作"""
        return DailyReportsDAO.delete(db, report_id)
