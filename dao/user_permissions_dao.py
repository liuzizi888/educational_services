"""
用户权限DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.user_permissions import UserPermissions


class UserPermissionsDAO:
    """用户权限数据访问对象"""

    @staticmethod
    def create(db: Session, username: str, password_hash: str, role: str) -> UserPermissions:
        """创建用户"""
        user = UserPermissions(
            username=username,
            password_hash=password_hash,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> UserPermissions:
        """根据ID查询用户"""
        return db.query(UserPermissions).filter(
            and_(
                UserPermissions.user_id == user_id,
                UserPermissions.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> UserPermissions:
        """根据用户名查询用户"""
        return db.query(UserPermissions).filter(
            and_(
                UserPermissions.username == username,
                UserPermissions.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10) -> tuple:
        """分页查询用户"""
        query = db.query(UserPermissions).filter(UserPermissions.is_deleted == 0)
        
        # 获取总数
        total = query.count()
        
        # 计算分页
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, user_id: int, username: str = None, password_hash: str = None, role: str = None) -> UserPermissions:
        """更新用户"""
        user = UserPermissionsDAO.get_by_id(db, user_id)
        if not user:
            return None
        
        if username is not None:
            user.username = username
        if password_hash is not None:
            user.password_hash = password_hash
        if role is not None:
            user.role = role
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """删除用户（软删除）"""
        user = UserPermissionsDAO.get_by_id(db, user_id)
        if not user:
            return False
        
        user.is_deleted = 1
        db.commit()
        return True

    @staticmethod
    def exists_by_username(db: Session, username: str, exclude_user_id: int = None) -> bool:
        """检查用户名是否存在"""
        query = db.query(UserPermissions).filter(
            and_(
                UserPermissions.username == username,
                UserPermissions.is_deleted == 0
            )
        )
        if exclude_user_id:
            query = query.filter(UserPermissions.user_id != exclude_user_id)
        return query.first() is not None
