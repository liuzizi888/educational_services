"""
员工日常工作API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.daily_reports import (
    DailyReportCreate,
    DailyReportUpdate,
    DailyReportResponse,
    DailyReportPageResponse
)
from service.daily_reports_service import DailyReportsService
from typing import Optional

router = APIRouter(tags=["员工日常工作"])


@router.post("", response_model=DailyReportResponse)
def create(obj: DailyReportCreate, db: Session = Depends(get_db)):
    """创建员工日常工作"""
    return DailyReportsService.create(db, obj)


@router.get("/page", response_model=DailyReportPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    report_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    report_date_start: Optional[str] = None,
    report_date_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询员工日常工作
    - report_id: 按日报ID精确查询
    - employee_id: 按员工ID筛选
    - report_date_start: 按日报日期起筛选 (格式: YYYY-MM-DD)
    - report_date_end: 按日报日期止筛选 (格式: YYYY-MM-DD)
    """
    return DailyReportsService.get_page(
        db, page, page_size, report_id, employee_id, report_date_start, report_date_end
    )


@router.put("/{report_id}", response_model=DailyReportResponse)
def update(report_id: int, obj: DailyReportUpdate, db: Session = Depends(get_db)):
    """更新员工日常工作"""
    result = DailyReportsService.update(db, report_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="员工日常工作不存在")
    return result


@router.delete("/{report_id}")
def delete(report_id: int, db: Session = Depends(get_db)):
    """删除员工日常工作（软删除）"""
    success = DailyReportsService.delete(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="员工日常工作不存在")
    return {"code": 200, "msg": "删除成功"}
