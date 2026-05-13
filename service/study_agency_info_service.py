"""
留学机构合作信息Service层
"""
from sqlalchemy.orm import Session
from dao.study_agency_info_dao import StudyAgencyInfoDAO
from schemas.study_agency_info import (
    StudyAgencyInfoCreate,
    StudyAgencyInfoUpdate,
    StudyAgencyInfoResponse,
    StudyAgencyInfoPageResponse
)
from typing import Optional


class StudyAgencyInfoService:
    """留学机构合作信息服务层"""

    @staticmethod
    def create(db: Session, obj: StudyAgencyInfoCreate) -> StudyAgencyInfoResponse:
        """创建机构"""
        obj_data = obj.model_dump()
        agency = StudyAgencyInfoDAO.create(db, obj_data)
        return StudyAgencyInfoResponse.model_validate(agency)

    @staticmethod
    def get_by_id(db: Session, agency_id: int) -> Optional[StudyAgencyInfoResponse]:
        """根据ID查询机构"""
        agency = StudyAgencyInfoDAO.get_by_id(db, agency_id)
        if agency:
            return StudyAgencyInfoResponse.model_validate(agency)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 agency_id: Optional[int] = None,
                 agency_name: Optional[str] = None,
                 country: Optional[str] = None,
                 cooperation_type: Optional[str] = None,
                 cooperation_status: Optional[str] = None) -> StudyAgencyInfoPageResponse:
        """分页查询机构"""
        items, total, page, page_size, total_pages = StudyAgencyInfoDAO.get_page(
            db, page, page_size, agency_id, agency_name, country, cooperation_type, cooperation_status
        )
        return StudyAgencyInfoPageResponse(
            items=[StudyAgencyInfoResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, agency_id: int, obj: StudyAgencyInfoUpdate) -> Optional[StudyAgencyInfoResponse]:
        """更新机构"""
        update_data = obj.model_dump(exclude_unset=True)
        agency = StudyAgencyInfoDAO.update(db, agency_id, update_data)
        if agency:
            return StudyAgencyInfoResponse.model_validate(agency)
        return None

    @staticmethod
    def delete(db: Session, agency_id: int) -> bool:
        """删除机构"""
        return StudyAgencyInfoDAO.delete(db, agency_id)
