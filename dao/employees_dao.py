"""
员工信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.employees import Employees
from typing import Optional, Tuple


class EmployeesDAO:
    """员工信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> Employees:
        """创建员工"""
        employee = Employees(**obj_data)
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    @staticmethod
    def get_by_id(db: Session, employee_id: int) -> Optional[Employees]:
        """根据ID查询员工"""
        return db.query(Employees).filter(
            and_(
                Employees.employee_id == employee_id,
                Employees.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10, 
                 employee_id: Optional[int] = None, 
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 position: Optional[str] = None) -> Tuple:
        """分页查询员工，支持按主键、姓名、状态、职位筛选"""
        query = db.query(Employees).filter(Employees.is_deleted == 0)
        
        # 添加筛选条件
        if employee_id is not None:
            query = query.filter(Employees.employee_id == employee_id)
        if name:
            query = query.filter(Employees.name.like(f"%{name}%"))
        if status:
            query = query.filter(Employees.status == status)
        if position:
            query = query.filter(Employees.position.like(f"%{position}%"))
        
        # 获取总数
        total = query.count()
        
        # 计算分页
        offset = (page - 1) * page_size
        items = query.order_by(Employees.employee_id.desc()).offset(offset).limit(page_size).all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, employee_id: int, update_data: dict) -> Optional[Employees]:
        """更新员工"""
        employee = EmployeesDAO.get_by_id(db, employee_id)
        if not employee:
            return None
        
        for key, value in update_data.items():
            if value is not None and hasattr(employee, key):
                setattr(employee, key, value)
        
        db.commit()
        db.refresh(employee)
        return employee

    @staticmethod
    def delete(db: Session, employee_id: int) -> bool:
        """删除员工（软删除）"""
        employee = EmployeesDAO.get_by_id(db, employee_id)
        if not employee:
            return False
        
        employee.is_deleted = 1
        db.commit()
        return True
