"""
全球留学政策Service层
"""
from sqlalchemy.orm import Session
from dao.global_study_policies_dao import GlobalStudyPoliciesDAO
from schemas.global_study_policies import (
    GlobalStudyPolicyCreate,
    GlobalStudyPolicyUpdate,
    GlobalStudyPolicyResponse,
    GlobalStudyPolicyPageResponse
)
from typing import Optional


class GlobalStudyPoliciesService:
    """全球留学政策服务层"""

    @staticmethod
    def create(db: Session, obj: GlobalStudyPolicyCreate) -> GlobalStudyPolicyResponse:
        """创建政策"""
        obj_data = obj.model_dump()
        policy = GlobalStudyPoliciesDAO.create(db, obj_data)
        return GlobalStudyPolicyResponse.model_validate(policy)

    @staticmethod
    def get_by_id(db: Session, policy_id: int) -> Optional[GlobalStudyPolicyResponse]:
        """根据ID查询政策"""
        policy = GlobalStudyPoliciesDAO.get_by_id(db, policy_id)
        if policy:
            return GlobalStudyPolicyResponse.model_validate(policy)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                  policy_id: Optional[int] = None,
                  country: Optional[str] = None,
                  policy_category: Optional[str] = None,
                  policy_type: Optional[str] = None,
                  impact_level: Optional[str] = None) -> GlobalStudyPolicyPageResponse:
        """分页查询政策"""
        items, total, page, page_size, total_pages = GlobalStudyPoliciesDAO.get_page(
            db, page, page_size, policy_id, country, policy_category, policy_type, impact_level
        )
        return GlobalStudyPolicyPageResponse(
            items=[GlobalStudyPolicyResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, policy_id: int, obj: GlobalStudyPolicyUpdate) -> Optional[GlobalStudyPolicyResponse]:
        """更新政策"""
        update_data = obj.model_dump(exclude_unset=True)
        policy = GlobalStudyPoliciesDAO.update(db, policy_id, update_data)
        if policy:
            return GlobalStudyPolicyResponse.model_validate(policy)
        return None

    @staticmethod
    def delete(db: Session, policy_id: int) -> bool:
        """删除政策"""
        return GlobalStudyPoliciesDAO.delete(db, policy_id)
