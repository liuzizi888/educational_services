"""
全球留学政策API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.global_study_policies import (
    GlobalStudyPolicyCreate,
    GlobalStudyPolicyUpdate,
    GlobalStudyPolicyResponse,
    GlobalStudyPolicyPageResponse
)
from service.global_study_policies_service import GlobalStudyPoliciesService
from typing import Optional

router = APIRouter(tags=["留学政策"])


@router.post("", response_model=GlobalStudyPolicyResponse)
def create(obj: GlobalStudyPolicyCreate, db: Session = Depends(get_db)):
    """创建留学政策"""
    return GlobalStudyPoliciesService.create(db, obj)


@router.get("/page", response_model=GlobalStudyPolicyPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    policy_id: Optional[int] = None,
    country: Optional[str] = None,
    policy_category: Optional[str] = None,
    policy_type: Optional[str] = None,
    impact_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询留学政策
    - policy_id: 按政策ID精确查询
    - country: 按国家/地区模糊查询
    - policy_category: 按政策分类筛选
    - policy_type: 按政策倾向筛选 (favorable/tightening/neutral)
    - impact_level: 按影响程度筛选 (low/medium/high)
    """
    return GlobalStudyPoliciesService.get_page(
        db, page, page_size, policy_id, country, policy_category, policy_type, impact_level
    )


@router.get("/{policy_id}", response_model=GlobalStudyPolicyResponse)
def get_by_id(policy_id: int, db: Session = Depends(get_db)):
    """根据ID查询留学政策"""
    result = GlobalStudyPoliciesService.get_by_id(db, policy_id)
    if not result:
        raise HTTPException(status_code=404, detail="政策不存在")
    return result


@router.put("/{policy_id}", response_model=GlobalStudyPolicyResponse)
def update(policy_id: int, obj: GlobalStudyPolicyUpdate, db: Session = Depends(get_db)):
    """更新留学政策"""
    result = GlobalStudyPoliciesService.update(db, policy_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="政策不存在")
    return result


@router.delete("/{policy_id}")
def delete(policy_id: int, db: Session = Depends(get_db)):
    """删除留学政策（软删除）"""
    success = GlobalStudyPoliciesService.delete(db, policy_id)
    if not success:
        raise HTTPException(status_code=404, detail="政策不存在")
    return {"code": 200, "msg": "删除成功"}
