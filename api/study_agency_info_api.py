"""
留学机构合作信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.study_agency_info import (
    StudyAgencyInfoCreate,
    StudyAgencyInfoUpdate,
    StudyAgencyInfoResponse,
    StudyAgencyInfoPageResponse
)
from service.study_agency_info_service import StudyAgencyInfoService
from typing import Optional

router = APIRouter(tags=["留学机构"])


@router.post("", response_model=StudyAgencyInfoResponse)
def create(obj: StudyAgencyInfoCreate, db: Session = Depends(get_db)):
    """创建留学机构"""
    return StudyAgencyInfoService.create(db, obj)


@router.get("/page", response_model=StudyAgencyInfoPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    agency_id: Optional[int] = None,
    agency_name: Optional[str] = None,
    country: Optional[str] = None,
    cooperation_type: Optional[str] = None,
    cooperation_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询留学机构
    - agency_id: 按机构ID精确查询
    - agency_name: 按机构名称模糊查询
    - country: 按国家模糊查询
    - cooperation_type: 按合作类型筛选 (university/agent/language_school/service_provider)
    - cooperation_status: 按合作状态筛选 (active/pending/terminated)
    """
    return StudyAgencyInfoService.get_page(
        db, page, page_size, agency_id, agency_name, country, cooperation_type, cooperation_status
    )


@router.get("/{agency_id}", response_model=StudyAgencyInfoResponse)
def get_by_id(agency_id: int, db: Session = Depends(get_db)):
    """根据ID查询留学机构"""
    result = StudyAgencyInfoService.get_by_id(db, agency_id)
    if not result:
        raise HTTPException(status_code=404, detail="机构不存在")
    return result


@router.put("/{agency_id}", response_model=StudyAgencyInfoResponse)
def update(agency_id: int, obj: StudyAgencyInfoUpdate, db: Session = Depends(get_db)):
    """更新留学机构"""
    result = StudyAgencyInfoService.update(db, agency_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="机构不存在")
    return result


@router.delete("/{agency_id}")
def delete(agency_id: int, db: Session = Depends(get_db)):
    """删除留学机构（软删除）"""
    success = StudyAgencyInfoService.delete(db, agency_id)
    if not success:
        raise HTTPException(status_code=404, detail="机构不存在")
    return {"code": 200, "msg": "删除成功"}
