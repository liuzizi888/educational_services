"""
留学机构合作信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.study_agency_info import StudyAgencyInfo
from typing import Optional, Tuple


class StudyAgencyInfoDAO:
    """留学机构合作信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudyAgencyInfo:
        """创建机构"""
        agency = StudyAgencyInfo(**obj_data)
        db.add(agency)
        db.commit()
        db.refresh(agency)
        return agency

    @staticmethod
    def get_by_id(db: Session, agency_id: int) -> Optional[StudyAgencyInfo]:
        """根据ID查询机构"""
        return db.query(StudyAgencyInfo).filter(
            and_(
                StudyAgencyInfo.agency_id == agency_id,
                StudyAgencyInfo.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 agency_id: Optional[int] = None,
                 agency_name: Optional[str] = None,
                 country: Optional[str] = None,
                 cooperation_type: Optional[str] = None,
                 cooperation_status: Optional[str] = None) -> Tuple:
        """分页查询机构"""
        query = db.query(StudyAgencyInfo).filter(StudyAgencyInfo.is_deleted == 0)

        if agency_id is not None:
            query = query.filter(StudyAgencyInfo.agency_id == agency_id)
        if agency_name:
            query = query.filter(StudyAgencyInfo.agency_name.like(f"%{agency_name}%"))
        if country:
            query = query.filter(StudyAgencyInfo.country.like(f"%{country}%"))
        if cooperation_type:
            query = query.filter(StudyAgencyInfo.cooperation_type == cooperation_type)
        if cooperation_status:
            query = query.filter(StudyAgencyInfo.cooperation_status == cooperation_status)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudyAgencyInfo.agency_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, agency_id: int, update_data: dict) -> Optional[StudyAgencyInfo]:
        """更新机构"""
        agency = StudyAgencyInfoDAO.get_by_id(db, agency_id)
        if not agency:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(agency, key):
                setattr(agency, key, value)

        db.commit()
        db.refresh(agency)
        return agency

    @staticmethod
    def delete(db: Session, agency_id: int) -> bool:
        """删除机构（软删除）"""
        agency = StudyAgencyInfoDAO.get_by_id(db, agency_id)
        if not agency:
            return False

        agency.is_deleted = 1
        db.commit()
        return True
