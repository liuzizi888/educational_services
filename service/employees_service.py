"""
员工信息服务层
"""
from sqlalchemy.orm import Session
from dao.employees_dao import EmployeesDAO
from schemas.employees import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeePageResponse
from typing import Optional


class EmployeesService:
    """员工信息服务层"""

    @staticmethod
    def create(db: Session, obj: EmployeeCreate) -> EmployeeResponse:
        """创建员工"""
        obj_data = obj.model_dump()
        employee = EmployeesDAO.create(db, obj_data)
        return EmployeeResponse.model_validate(employee)

    @staticmethod
    def get_by_id(db: Session, employee_id: int) -> Optional[EmployeeResponse]:
        """根据ID查询员工"""
        employee = EmployeesDAO.get_by_id(db, employee_id)
        if employee:
            return EmployeeResponse.model_validate(employee)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 employee_id: Optional[int] = None,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 position: Optional[str] = None) -> EmployeePageResponse:
        """分页查询员工"""
        items, total, page, page_size, total_pages = EmployeesDAO.get_page(
            db, page, page_size, employee_id, name, status, position
        )
        return EmployeePageResponse(
            items=[EmployeeResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, employee_id: int, obj: EmployeeUpdate) -> Optional[EmployeeResponse]:
        """更新员工"""
        update_data = obj.model_dump(exclude_unset=True)
        employee = EmployeesDAO.update(db, employee_id, update_data)
        if employee:
            return EmployeeResponse.model_validate(employee)
        return None

    @staticmethod
    def delete(db: Session, employee_id: int) -> bool:
        """删除员工"""
        return EmployeesDAO.delete(db, employee_id)
