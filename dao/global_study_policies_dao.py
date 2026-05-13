"""
全球留学政策DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.global_study_policies import GlobalStudyPolicies
from typing import Optional, Tuple


class GlobalStudyPoliciesDAO:
    """全球留学政策数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> GlobalStudyPolicies:
        """创建政策"""
        policy = GlobalStudyPolicies(**obj_data)
        db.add(policy)
        db.commit()
        db.refresh(policy)
        return policy

    @staticmethod
    def get_by_id(db: Session, policy_id: int) -> Optional[GlobalStudyPolicies]:
        """根据ID查询政策"""
        return db.query(GlobalStudyPolicies).filter(
            and_(
                GlobalStudyPolicies.policy_id == policy_id,
                GlobalStudyPolicies.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 policy_id: Optional[int] = None,
                 country: Optional[str] = None,
                 policy_category: Optional[str] = None,
                 policy_type: Optional[str] = None,
                 impact_level: Optional[str] = None) -> Tuple:
        """分页查询政策"""
        query = db.query(GlobalStudyPolicies).filter(GlobalStudyPolicies.is_deleted == 0)

        if policy_id is not None:
            query = query.filter(GlobalStudyPolicies.policy_id == policy_id)
        if country:
            query = query.filter(GlobalStudyPolicies.country.like(f"%{country}%"))
        if policy_category:
            query = query.filter(GlobalStudyPolicies.policy_category == policy_category)
        if policy_type:
            query = query.filter(GlobalStudyPolicies.policy_type == policy_type)
        if impact_level:
            query = query.filter(GlobalStudyPolicies.impact_level == impact_level)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(GlobalStudyPolicies.policy_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, policy_id: int, update_data: dict) -> Optional[GlobalStudyPolicies]:
        """更新政策"""
        policy = GlobalStudyPoliciesDAO.get_by_id(db, policy_id)
        if not policy:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(policy, key):
                setattr(policy, key, value)

        db.commit()
        db.refresh(policy)
        return policy

    @staticmethod
    def delete(db: Session, policy_id: int) -> bool:
        """删除政策（软删除）"""
        policy = GlobalStudyPoliciesDAO.get_by_id(db, policy_id)
        if not policy:
            return False

        policy.is_deleted = 1
        db.commit()
        return True
