"""
客户信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.clients import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    ClientPageResponse
)
from service.clients_service import ClientsService
from typing import Optional

# 创建路由器
router = APIRouter(tags=["客户管理"])


@router.post("", response_model=ClientResponse)
def create(obj: ClientCreate, db: Session = Depends(get_db)):
    """创建客户"""
    return ClientsService.create(db, obj)


@router.get("/page", response_model=ClientPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    client_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    assigned_employee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """分页查询客户
    - client_id: 按客户ID精确查询
    - name: 按姓名模糊查询
    - status: 按流转状态筛选 (new/contacted/signed/lost)
    - assigned_employee_id: 按负责员工ID筛选
    """
    return ClientsService.get_page(db, page, page_size, client_id, name, status, assigned_employee_id)


@router.get("/{client_id}", response_model=ClientResponse)
def get_by_id(client_id: int, db: Session = Depends(get_db)):
    """根据ID查询客户"""
    result = ClientsService.get_by_id(db, client_id)
    if not result:
        raise HTTPException(status_code=404, detail="客户不存在")
    return result


@router.put("/{client_id}", response_model=ClientResponse)
def update(client_id: int, obj: ClientUpdate, db: Session = Depends(get_db)):
    """更新客户"""
    result = ClientsService.update(db, client_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="客户不存在")
    return result


@router.delete("/{client_id}")
def delete(client_id: int, db: Session = Depends(get_db)):
    """删除客户（软删除）"""
    success = ClientsService.delete(db, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="客户不存在")
    return {"code": 200, "msg": "删除成功"}
