"""
测试用户注册和登录功能
"""
from db.database import Session
from schemas.user_permissions import UserPermissionsCreate, LoginRequest
from service.user_permissions_service import UserPermissionsService
from utils.password import hash_password, verify_password


def test_password():
    """测试密码加密和验证"""
    print("=" * 50)
    print("测试密码加密和验证")
    print("=" * 50)
    
    password = "admin123"
    hashed = hash_password(password)
    
    print(f"原始密码: {password}")
    print(f"加密后: {hashed}")
    print(f"验证成功: {verify_password(password, hashed)}")
    print(f"验证失败(错误密码): {verify_password('wrong', hashed)}")
    print()


def test_create_user():
    """测试创建用户"""
    print("=" * 50)
    print("测试创建用户")
    print("=" * 50)
    
    db = Session()
    try:
        # 创建测试用户
        user_data = UserPermissionsCreate(
            username="test_admin",
            password="admin123",
            role="admin"
        )
        
        user = UserPermissionsService.create(db, user_data)
        print(f"创建用户成功: {user}")
        print(f"用户ID: {user.user_id}")
        print(f"用户名: {user.username}")
        print(f"角色: {user.role}")
        
    except ValueError as e:
        print(f"创建用户失败: {e}")
    finally:
        db.close()
    
    print()


def test_login():
    """测试用户登录"""
    print("=" * 50)
    print("测试用户登录")
    print("=" * 50)
    
    db = Session()
    try:
        # 测试登录
        result = UserPermissionsService.login(db, "test_admin", "admin123")
        print(f"登录成功!")
        print(f"用户ID: {result.user_id}")
        print(f"用户名: {result.username}")
        print(f"角色: {result.role}")
        
    except ValueError as e:
        print(f"登录失败: {e}")
    finally:
        db.close()
    
    print()


def test_get_page():
    """测试分页查询"""
    print("=" * 50)
    print("测试分页查询")
    print("=" * 50)
    
    db = Session()
    try:
        # 分页查询
        page_result = UserPermissionsService.get_page(db, page=1, page_size=10)
        print(f"总数: {page_result.total}")
        print(f"当前页: {page_result.page}")
        print(f"每页大小: {page_result.page_size}")
        print(f"总页数: {page_result.total_pages}")
        print(f"用户列表:")
        for user in page_result.items:
            print(f"  - {user.username} ({user.role})")
        
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        db.close()
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("开始测试")
    print("=" * 50 + "\n")
    
    # 测试密码功能
    test_password()
    
    # 测试创建用户
    test_create_user()
    
    # 测试登录
    test_login()
    
    # 测试分页查询
    test_get_page()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
