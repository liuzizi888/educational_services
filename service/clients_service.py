"""
客户信息服务层
"""
from sqlalchemy.orm import Session
from dao.clients_dao import ClientsDAO
from schemas.clients import ClientCreate, ClientUpdate, ClientResponse, ClientPageResponse
from typing import Optional


class ClientsService:
    """客户信息服务层"""

    @staticmethod
    def create(db: Session, obj: ClientCreate) -> ClientResponse:
        """创建客户"""
        obj_data = obj.model_dump()
        client = ClientsDAO.create(db, obj_data)
        return ClientResponse.model_validate(client)

    @staticmethod
    def get_by_id(db: Session, client_id: int) -> Optional[ClientResponse]:
        """根据ID查询客户"""
        client = ClientsDAO.get_by_id(db, client_id)
        if client:
            return ClientResponse.model_validate(client)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 client_id: Optional[int] = None,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 assigned_employee_id: Optional[int] = None) -> ClientPageResponse:
        """分页查询客户"""
        items, total, page, page_size, total_pages = ClientsDAO.get_page(
            db, page, page_size, client_id, name, status, assigned_employee_id
        )
        return ClientPageResponse(
            items=[ClientResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, client_id: int, obj: ClientUpdate) -> Optional[ClientResponse]:
        """更新客户"""
        update_data = obj.model_dump(exclude_unset=True)
        client = ClientsDAO.update(db, client_id, update_data)
        if client:
            return ClientResponse.model_validate(client)
        return None

    @staticmethod
    def delete(db: Session, client_id: int) -> bool:
        """删除客户"""
        return ClientsDAO.delete(db, client_id)
