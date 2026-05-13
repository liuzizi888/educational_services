"""
用户权限API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user_permissions import (
    UserPermissionsCreate, 
    UserPermissionsUpdate, 
    UserPermissionsResponse, 
    UserPermissionsPageResponse,
    LoginRequest,
    LoginResponse
)
from service.user_permissions_service import UserPermissionsService
from utils.auth_middleware import get_current_user
from datetime import datetime, timedelta
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
from dotenv import load_dotenv

load_dotenv()

# 获取AES密钥和IV
AES_KEY = os.getenv('AES_KEY', '1234567890123456').encode()
AES_IV = os.getenv('AES_IV', '1234567890123456').encode()

# 创建路由器
router = APIRouter(tags=["用户权限"])


def generate_token(user_id: int, role: str, expire_hours: int = 24) -> str:
    """
    生成JWT Token
    
    Args:
        user_id: 用户ID
        role: 用户角色
        expire_hours: 过期时间（小时）
    
    Returns:
        str: 加密的Token
    """
    expire_timestamp = int((datetime.now() + timedelta(hours=expire_hours)).timestamp())
    
    payload = {
        "uid": user_id,
        "role": role,
        "exp": expire_timestamp
    }
    
    # 转换为JSON字符串
    json_str = json.dumps(payload)
    json_bytes = json_str.encode()
    
    # PKCS7填充
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(json_bytes) + padder.finalize()
    
    # AES加密
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Base64编码
    token = base64.b64encode(encrypted).decode()
    
    return token


@router.post("", response_model=UserPermissionsResponse)
def create(obj: UserPermissionsCreate, db: Session = Depends(get_db)):
    """创建用户"""
    try:
        return UserPermissionsService.create(db, obj)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/page", response_model=UserPermissionsPageResponse)
def get_page(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """分页查询用户"""
    return UserPermissionsService.get_page(db, page, page_size)


@router.get("/{user_id}", response_model=UserPermissionsResponse)
def get_by_id(user_id: int, db: Session = Depends(get_db)):
    """根据ID查询用户"""
    result = UserPermissionsService.get_by_id(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="用户不存在")
    return result


@router.put("/{user_id}", response_model=UserPermissionsResponse)
def update(user_id: int, obj: UserPermissionsUpdate, db: Session = Depends(get_db)):
    """更新用户"""
    try:
        result = UserPermissionsService.update(db, user_id, obj)
        if not result:
            raise HTTPException(status_code=404, detail="用户不存在")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    success = UserPermissionsService.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "msg": "删除成功"}


@router.post("/login", response_model=LoginResponse)
def login(obj: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    try:
        # 调用服务层进行登录验证
        login_result = UserPermissionsService.login(db, obj.username, obj.password)
        
        # 生成Token
        token = generate_token(
            user_id=login_result.user_id,
            role=login_result.role,
            expire_hours=24  # Token有效期24小时
        )
        
        # 返回完整的登录响应
        return LoginResponse(
            code=200,
            msg="登录成功",
            token=token,
            user_id=login_result.user_id,
            username=login_result.username,
            role=login_result.role
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
