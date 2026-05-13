"""
测试所有导入是否正常
"""
import sys

def test_imports():
    """测试所有模块的导入"""
    print("=" * 50)
    print("测试模块导入")
    print("=" * 50)
    
    modules = [
        ("db.database", "数据库连接"),
        ("models.user_permissions", "用户权限模型"),
        ("schemas.user_permissions", "用户权限Schema"),
        ("utils.password", "密码工具"),
        ("dao.user_permissions_dao", "用户权限DAO"),
        ("service.user_permissions_service", "用户权限服务"),
        ("api.user_permissions_api", "用户权限API"),
    ]
    
    errors = []
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✓ {description} ({module_name})")
        except Exception as e:
            print(f"✗ {description} ({module_name}): {e}")
            errors.append((module_name, str(e)))
    
    print()
    if errors:
        print("=" * 50)
        print(f"有 {len(errors)} 个模块导入失败")
        print("=" * 50)
        for module_name, error in errors:
            print(f"\n{module_name}:")
            print(f"  {error}")
        return False
    else:
        print("=" * 50)
        print("所有模块导入成功！")
        print("=" * 50)
        return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
