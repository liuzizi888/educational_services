"""
用户权限Service层
"""
from sqlalchemy.orm import Session
from dao.user_permissions_dao import UserPermissionsDAO
from utils.password import hash_password, verify_password
from schemas.user_permissions import UserPermissionsCreate, UserPermissionsUpdate, UserPermissionsResponse, UserPermissionsPageResponse, LoginResponse


class UserPermissionsService:
    """用户权限服务"""

    @staticmethod
    def create(db: Session, obj: UserPermissionsCreate) -> UserPermissionsResponse:
        """创建用户"""
        # 检查用户名是否已存在
        if UserPermissionsDAO.exists_by_username(db, obj.username):
            raise ValueError(f"用户名 '{obj.username}' 已存在")
        
        # 密码加密
        password_hash = hash_password(obj.password)
        
        # 创建用户
        user = UserPermissionsDAO.create(
            db=db,
            username=obj.username,
            password_hash=password_hash,
            role=obj.role.value
        )
        
        return UserPermissionsResponse.model_validate(user)

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> UserPermissionsResponse:
        """根据ID查询用户"""
        user = UserPermissionsDAO.get_by_id(db, user_id)
        if not user:
            return None
        return UserPermissionsResponse.model_validate(user)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10) -> UserPermissionsPageResponse:
        """分页查询用户"""
        items, total, page, page_size, total_pages = UserPermissionsDAO.get_page(db, page, page_size)
        
        return UserPermissionsPageResponse(
            items=[UserPermissionsResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, user_id: int, obj: UserPermissionsUpdate) -> UserPermissionsResponse:
        """更新用户"""
        # 检查用户是否存在
        existing_user = UserPermissionsDAO.get_by_id(db, user_id)
        if not existing_user:
            return None
        
        # 如果要更新用户名，检查是否与其他用户冲突
        if obj.username and obj.username != existing_user.username:
            if UserPermissionsDAO.exists_by_username(db, obj.username, exclude_user_id=user_id):
                raise ValueError(f"用户名 '{obj.username}' 已存在")
        
        # 密码加密（如果提供了新密码）
        password_hash = None
        if obj.password:
            password_hash = hash_password(obj.password)
        
        # 更新用户
        user = UserPermissionsDAO.update(
            db=db,
            user_id=user_id,
            username=obj.username,
            password_hash=password_hash,
            role=obj.role.value if obj.role else None
        )
        
        return UserPermissionsResponse.model_validate(user)

    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """删除用户"""
        return UserPermissionsDAO.delete(db, user_id)

    @staticmethod
    def login(db: Session, username: str, password: str) -> LoginResponse:
        """用户登录"""
        # 查询用户
        user = UserPermissionsDAO.get_by_username(db, username)
        if not user:
            raise ValueError("用户名或密码错误")
        
        # 验证密码
        if not verify_password(password, user.password_hash):
            raise ValueError("用户名或密码错误")
        
        return LoginResponse(
            code=200,
            msg="登录成功",
            token="",  # Token将由API层生成
            user_id=user.user_id,
            username=user.username,
            role=user.role
        )
