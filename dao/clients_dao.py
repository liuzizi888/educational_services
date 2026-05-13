"""
客户信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.clients import Clients
from typing import Optional, Tuple


class ClientsDAO:
    """客户信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> Clients:
        """创建客户"""
        client = Clients(**obj_data)
        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def get_by_id(db: Session, client_id: int) -> Optional[Clients]:
        """根据ID查询客户"""
        return db.query(Clients).filter(
            and_(
                Clients.client_id == client_id,
                Clients.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 client_id: Optional[int] = None,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 assigned_employee_id: Optional[int] = None) -> Tuple:
        """分页查询客户，支持按主键、姓名、状态、负责员工筛选"""
        query = db.query(Clients).filter(Clients.is_deleted == 0)

        # 添加筛选条件
        if client_id is not None:
            query = query.filter(Clients.client_id == client_id)
        if name:
            query = query.filter(Clients.name.like(f"%{name}%"))
        if status:
            query = query.filter(Clients.status == status)
        if assigned_employee_id is not None:
            query = query.filter(Clients.assigned_employee_id == assigned_employee_id)

        # 获取总数
        total = query.count()

        # 计算分页
        offset = (page - 1) * page_size
        items = query.order_by(Clients.client_id.desc()).offset(offset).limit(page_size).all()

        # 计算总页数
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, client_id: int, update_data: dict) -> Optional[Clients]:
        """更新客户"""
        client = ClientsDAO.get_by_id(db, client_id)
        if not client:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(client, key):
                setattr(client, key, value)

        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete(db: Session, client_id: int) -> bool:
        """删除客户（软删除）"""
        client = ClientsDAO.get_by_id(db, client_id)
        if not client:
            return False

        client.is_deleted = 1
        db.commit()
        return True
