"""
员工信息API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.employees import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeePageResponse
)
from service.employees_service import EmployeesService
from typing import Optional

# 创建路由器
router = APIRouter(tags=["员工管理"])


@router.post("", response_model=EmployeeResponse)
def create(obj: EmployeeCreate, db: Session = Depends(get_db)):
    """创建员工"""
    return EmployeesService.create(db, obj)


@router.get("/page", response_model=EmployeePageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    employee_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    position: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询员工
    - employee_id: 按员工ID精确查询
    - name: 按姓名模糊查询
    - status: 按在职状态筛选 (active/resigned)
    - position: 按职位模糊查询
    """
    return EmployeesService.get_page(db, page, page_size, employee_id, name, status, position)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_by_id(employee_id: int, db: Session = Depends(get_db)):
    """根据ID查询员工"""
    result = EmployeesService.get_by_id(db, employee_id)
    if not result:
        raise HTTPException(status_code=404, detail="员工不存在")
    return result


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update(employee_id: int, obj: EmployeeUpdate, db: Session = Depends(get_db)):
    """更新员工"""
    result = EmployeesService.update(db, employee_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="员工不存在")
    return result


@router.delete("/{employee_id}")
def delete(employee_id: int, db: Session = Depends(get_db)):
    """删除员工（软删除）"""
    success = EmployeesService.delete(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="员工不存在")
    return {"code": 200, "msg": "删除成功"}
