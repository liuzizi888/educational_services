# 用户权限API使用说明

## 安装依赖

首先安装所需的Python包：

```bash
pip install -r requirements.txt
```

## 初始化数据库

运行数据库初始化脚本，创建所需的表结构：

```bash
python init_db.py
```

## 测试功能

运行测试脚本，测试用户注册和登录功能：

```bash
python test_user.py
```

## API接口说明

### 1. 用户注册（创建用户）

**接口地址**: `POST /user_permissions`

**请求体**:
```json
{
    "username": "test_user",
    "password": "password123",
    "role": "admin"
}
```

**角色可选值**:
- `admin` - 管理员
- `employee` - 员工
- `student` - 学生
- `teacher` - 教师

**响应示例**:
```json
{
    "user_id": 1,
    "username": "test_user",
    "role": "admin",
    "is_deleted": 0,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
}
```

### 2. 用户登录

**接口地址**: `POST /user_permissions/login`

**请求体**:
```json
{
    "username": "test_user",
    "password": "password123"
}
```

**响应示例**:
```json
{
    "code": 200,
    "msg": "登录成功",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_id": 1,
    "username": "test_user",
    "role": "admin"
}
```

**重要**: 登录成功后返回的 `token` 需要在后续请求的Header中携带：
```
Authorization: Bearer <token>
```

### 3. 查询单个用户

**接口地址**: `GET /user_permissions/{user_id}`

**响应示例**:
```json
{
    "user_id": 1,
    "username": "test_user",
    "role": "admin",
    "is_deleted": 0,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
}
```

### 4. 分页查询用户

**接口地址**: `GET /user_permissions/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）

**响应示例**:
```json
{
    "items": [
        {
            "user_id": 1,
            "username": "test_user",
            "role": "admin",
            "is_deleted": 0,
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 5. 更新用户

**接口地址**: `PUT /user_permissions/{user_id}`

**请求体** (所有字段可选):
```json
{
    "username": "new_username",
    "password": "new_password",
    "role": "teacher"
}
```

**响应示例**:
```json
{
    "user_id": 1,
    "username": "new_username",
    "role": "teacher",
    "is_deleted": 0,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:30:00"
}
```

### 6. 删除用户

**接口地址**: `DELETE /user_permissions/{user_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

## 密码加密说明

密码使用bcrypt算法进行加密存储，确保安全性：

- **加密**: 使用 `hash_password(password)` 函数加密密码
- **验证**: 使用 `verify_password(plain_password, hashed_password)` 函数验证密码

加密示例：
```python
from utils.password import hash_password, verify_password

# 加密密码
hashed = hash_password("my_password")
# 输出: $2b$12$xxxxxx...

# 验证密码
is_valid = verify_password("my_password", hashed)
# 输出: True
```

## Token说明

登录成功后返回的Token使用AES加密，包含了用户ID和角色信息：

- **有效期**: 24小时
- **格式**: Base64编码的AES加密字符串

TokenPayload结构：
```json
{
    "uid": 1,
    "role": "admin",
    "exp": 1704067200
}
```

## 启动服务

```bash
python main.py
```

服务启动后，访问 `http://localhost:8888/docs` 查看Swagger API文档。

---

## 11. 员工日常工作API

### 11.1 创建员工日常工作

**接口地址**: `POST /daily_reports`

**请求体**:
```json
{
    "employee_id": 1,
    "report_date": "2024-01-15",
    "content": "完成了客户跟进工作",
    "work_hours": 8.5
}
```

**响应示例**:
```json
{
    "report_id": 1,
    "employee_id": 1,
    "report_date": "2024-01-15",
    "content": "完成了客户跟进工作",
    "work_hours": 8.5,
    "is_deleted": 0,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
}
```

### 11.2 分页查询员工日常工作

**接口地址**: `GET /daily_reports/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `report_id` - 按日报ID精确查询
- `employee_id` - 按员工ID筛选
- `report_date_start` - 按日报日期起筛选（格式: YYYY-MM-DD）
- `report_date_end` - 按日报日期止筛选（格式: YYYY-MM-DD）

**响应示例**:
```json
{
    "items": [
        {
            "report_id": 1,
            "employee_id": 1,
            "report_date": "2024-01-15",
            "content": "完成了客户跟进工作",
            "work_hours": 8.5,
            "is_deleted": 0,
            "created_at": "2024-01-15T10:00:00",
            "updated_at": "2024-01-15T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 11.3 更新员工日常工作

**接口地址**: `PUT /daily_reports/{report_id}`

**请求体** (所有字段可选):
```json
{
    "content": "更新后的日报内容",
    "work_hours": 9.0
}
```

**响应示例**:
```json
{
    "report_id": 1,
    "employee_id": 1,
    "report_date": "2024-01-15",
    "content": "更新后的日报内容",
    "work_hours": 9.0,
    "is_deleted": 0,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T14:00:00"
}
```

### 11.4 删除员工日常工作

**接口地址**: `DELETE /daily_reports/{report_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

---

## 12. 每月达成目标API

### 12.1 创建每月达成目标

**接口地址**: `POST /monthly_goals`

**请求体**:
```json
{
    "employee_id": 1,
    "target_month": "2026-05-01",
    "target_amount": 50000.00,
    "actual_amount": 45000.00,
    "achievement_rate": 90.00,
    "status": "pending"
}
```

**响应示例**:
```json
{
    "goal_id": 1,
    "employee_id": 1,
    "target_month": "2026-05-01",
    "target_amount": 50000.00,
    "actual_amount": 45000.00,
    "achievement_rate": 90.00,
    "status": "pending",
    "is_deleted": 0,
    "created_at": "2026-05-01T10:00:00",
    "updated_at": "2026-05-01T10:00:00"
}
```

### 12.2 分页查询每月达成目标

**接口地址**: `GET /monthly_goals/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `goal_id` - 按目标ID精确查询
- `employee_id` - 按员工ID筛选
- `status` - 按目标状态筛选 (pending/achieved/failed)
- `target_month_start` - 按目标月份起筛选（格式: YYYY-MM-DD）
- `target_month_end` - 按目标月份止筛选（格式: YYYY-MM-DD）

**响应示例**:
```json
{
    "items": [
        {
            "goal_id": 1,
            "employee_id": 1,
            "target_month": "2026-05-01",
            "target_amount": 50000.00,
            "actual_amount": 45000.00,
            "achievement_rate": 90.00,
            "status": "pending",
            "is_deleted": 0,
            "created_at": "2026-05-01T10:00:00",
            "updated_at": "2026-05-01T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 12.3 更新每月达成目标

**接口地址**: `PUT /monthly_goals/{goal_id}`

**请求体** (所有字段可选):
```json
{
    "actual_amount": 52000.00,
    "achievement_rate": 104.00,
    "status": "achieved"
}
```

**响应示例**:
```json
{
    "goal_id": 1,
    "employee_id": 1,
    "target_month": "2026-05-01",
    "target_amount": 50000.00,
    "actual_amount": 52000.00,
    "achievement_rate": 104.00,
    "status": "achieved",
    "is_deleted": 0,
    "created_at": "2026-05-01T10:00:00",
    "updated_at": "2026-05-31T18:00:00"
}
```

### 12.4 删除每月达成目标

**接口地址**: `DELETE /monthly_goals/{goal_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

---

## 13. 学生信息API

### 13.1 创建学生信息

**接口地址**: `POST /students`

**请求体**:
```json
{
    "name": "张三",
    "gender": "M",
    "dob": "2010-05-15",
    "class_id": 1,
    "email": "zhangsan@example.com",
    "parent_contact": "13800138000",
    "enrollment_date": "2024-09-01",
    "status": "enrolled"
}
```

**响应示例**:
```json
{
    "student_id": 1,
    "name": "张三",
    "gender": "M",
    "dob": "2010-05-15",
    "class_id": 1,
    "email": "zhangsan@example.com",
    "parent_contact": "13800138000",
    "enrollment_date": "2024-09-01",
    "status": "enrolled",
    "is_deleted": 0,
    "created_at": "2024-09-01T10:00:00",
    "updated_at": "2024-09-01T10:00:00"
}
```

### 13.2 分页查询学生信息

**接口地址**: `GET /students/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `student_id` - 按学生ID精确查询
- `class_id` - 按班级ID筛选
- `name` - 按学生姓名模糊查询
- `status` - 按学籍状态筛选 (enrolled/graduated/withdrawn)
- `enrollment_date_start` - 按入学日期起筛选（格式: YYYY-MM-DD）
- `enrollment_date_end` - 按入学日期止筛选（格式: YYYY-MM-DD）

**响应示例**:
```json
{
    "items": [
        {
            "student_id": 1,
            "name": "张三",
            "gender": "M",
            "dob": "2010-05-15",
            "class_id": 1,
            "email": "zhangsan@example.com",
            "parent_contact": "13800138000",
            "enrollment_date": "2024-09-01",
            "status": "enrolled",
            "is_deleted": 0,
            "created_at": "2024-09-01T10:00:00",
            "updated_at": "2024-09-01T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 13.3 更新学生信息

**接口地址**: `PUT /students/{student_id}`

**请求体** (所有字段可选):
```json
{
    "class_id": 2,
    "status": "graduated"
}
```

**响应示例**:
```json
{
    "student_id": 1,
    "name": "张三",
    "gender": "M",
    "dob": "2010-05-15",
    "class_id": 2,
    "email": "zhangsan@example.com",
    "parent_contact": "13800138000",
    "enrollment_date": "2024-09-01",
    "status": "graduated",
    "is_deleted": 0,
    "created_at": "2024-09-01T10:00:00",
    "updated_at": "2025-06-30T18:00:00"
}
```

### 13.4 删除学生信息

**接口地址**: `DELETE /students/{student_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

---

## 14. 学生人脸识别API

### 14.1 创建学生人脸识别

**接口地址**: `POST /student_face_records`

**请求体**:
```json
{
    "student_id": 1,
    "face_feature_data": "base64_encoded_feature_vector...",
    "photo_url": "/uploads/faces/student_001.jpg"
}
```

**响应示例**:
```json
{
    "face_id": 1,
    "student_id": 1,
    "face_feature_data": "base64_encoded_feature_vector...",
    "photo_url": "/uploads/faces/student_001.jpg",
    "is_deleted": 0,
    "created_at": "2024-09-01T10:00:00",
    "updated_at": "2024-09-01T10:00:00"
}
```

### 14.2 分页查询学生人脸识别

**接口地址**: `GET /student_face_records/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `face_id` - 按人脸记录ID精确查询
- `student_id` - 按学生ID筛选

**响应示例**:
```json
{
    "items": [
        {
            "face_id": 1,
            "student_id": 1,
            "face_feature_data": "base64_encoded_feature_vector...",
            "photo_url": "/uploads/faces/student_001.jpg",
            "is_deleted": 0,
            "created_at": "2024-09-01T10:00:00",
            "updated_at": "2024-09-01T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 14.3 更新学生人脸识别

**接口地址**: `PUT /student_face_records/{face_id}`

**请求体** (所有字段可选):
```json
{
    "face_feature_data": "new_base64_encoded_feature_vector...",
    "photo_url": "/uploads/faces/student_001_updated.jpg"
}
```

**响应示例**:
```json
{
    "face_id": 1,
    "student_id": 1,
    "face_feature_data": "new_base64_encoded_feature_vector...",
    "photo_url": "/uploads/faces/student_001_updated.jpg",
    "is_deleted": 0,
    "created_at": "2024-09-01T10:00:00",
    "updated_at": "2024-09-02T15:00:00"
}
```

### 14.4 删除学生人脸识别

**接口地址**: `DELETE /student_face_records/{face_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

---

## 16. 学生请假API

### 16.1 创建学生请假

**接口地址**: `POST /student_leaves`

**请求体**:
```json
{
    "student_id": 1,
    "start_time": "2024-09-15T08:00:00",
    "end_time": "2024-09-16T18:00:00",
    "reason": "身体不适，需要休息",
    "approver_id": 2
}
```

**响应示例**:
```json
{
    "leave_id": 1,
    "student_id": 1,
    "start_time": "2024-09-15T08:00:00",
    "end_time": "2024-09-16T18:00:00",
    "reason": "身体不适，需要休息",
    "status": "pending",
    "approver_id": 2,
    "is_deleted": 0,
    "created_at": "2024-09-14T10:00:00",
    "updated_at": "2024-09-14T10:00:00"
}
```

### 16.2 分页查询学生请假

**接口地址**: `GET /student_leaves/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `leave_id` - 按请假ID精确查询
- `student_id` - 按学生ID筛选
- `approver_id` - 按审批人ID筛选
- `status` - 按审批状态筛选 (pending/approved/rejected)
- `start_time_start` - 按请假开始时间起筛选（格式: YYYY-MM-DD HH:MM:SS）
- `start_time_end` - 按请假开始时间止筛选（格式: YYYY-MM-DD HH:MM:SS）

**响应示例**:
```json
{
    "items": [
        {
            "leave_id": 1,
            "student_id": 1,
            "start_time": "2024-09-15T08:00:00",
            "end_time": "2024-09-16T18:00:00",
            "reason": "身体不适，需要休息",
            "status": "pending",
            "approver_id": 2,
            "is_deleted": 0,
            "created_at": "2024-09-14T10:00:00",
            "updated_at": "2024-09-14T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 16.3 更新学生请假

**接口地址**: `PUT /student_leaves/{leave_id}`

**请求体** (所有字段可选):
```json
{
    "status": "approved"
}
```

**响应示例**:
```json
{
    "leave_id": 1,
    "student_id": 1,
    "start_time": "2024-09-15T08:00:00",
    "end_time": "2024-09-16T18:00:00",
    "reason": "身体不适，需要休息",
    "status": "approved",
    "approver_id": 2,
    "is_deleted": 0,
    "created_at": "2024-09-14T10:00:00",
    "updated_at": "2024-09-14T14:00:00"
}
```

### 16.4 删除学生请假

**接口地址**: `DELETE /student_leaves/{leave_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

---

## 17. 学生投诉建议API

### 17.1 创建学生投诉、建议

**接口地址**: `POST /student_complaints`

**请求体**:
```json
{
    "student_id": 1,
    "content": "希望增加更多的自习室",
    "type": "suggestions",
    "handler_id": 2
}
```

**响应示例**:
```json
{
    "complaint_id": 1,
    "student_id": 1,
    "content": "希望增加更多的自习室",
    "type": "suggestions",
    "status": "pending",
    "handler_id": 2,
    "resolve_remark": null,
    "is_deleted": 0,
    "created_at": "2024-09-15T10:00:00",
    "updated_at": "2024-09-15T10:00:00"
}
```

### 17.2 分页查询学生投诉、建议

**接口地址**: `GET /student_complaints/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `complaint_id` - 按投诉ID精确查询
- `student_id` - 按学生ID筛选
- `type` - 按类型筛选 (complaints/suggestions)
- `status` - 按处理状态筛选 (pending/processing/resolved/rejected)
- `handler_id` - 按处理人ID筛选
- `created_at_start` - 按创建时间起筛选（格式: YYYY-MM-DD HH:MM:SS）
- `created_at_end` - 按创建时间止筛选（格式: YYYY-MM-DD HH:MM:SS）

**响应示例**:
```json
{
    "items": [
        {
            "complaint_id": 1,
            "student_id": 1,
            "content": "希望增加更多的自习室",
            "type": "suggestions",
            "status": "pending",
            "handler_id": 2,
            "resolve_remark": null,
            "is_deleted": 0,
            "created_at": "2024-09-15T10:00:00",
            "updated_at": "2024-09-15T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 17.3 更新学生投诉、建议

**接口地址**: `PUT /student_complaints/{complaint_id}`

**请求体** (所有字段可选):
```json
{
    "status": "resolved",
    "resolve_remark": "已安排增加自习室资源"
}
```

**响应示例**:
```json
{
    "complaint_id": 1,
    "student_id": 1,
    "content": "希望增加更多的自习室",
    "type": "suggestions",
    "status": "resolved",
    "handler_id": 2,
    "resolve_remark": "已安排增加自习室资源",
    "is_deleted": 0,
    "created_at": "2024-09-15T10:00:00",
    "updated_at": "2024-09-15T14:00:00"
}
```

### 17.4 删除学生投诉、建议

**接口地址**: `DELETE /student_complaints/{complaint_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

---

## 18. 班级信息API

### 18.1 创建班级信息

**接口地址**: `POST /classes`

**请求体**:
```json
{
    "class_name": "2026届A班",
    "grade_level": "高一",
    "head_teacher_id": 5,
    "classroom_location": "教学楼101",
    "max_students": 40,
    "current_students": 35,
    "status": "active"
}
```

**响应示例**:
```json
{
    "class_id": 1,
    "class_name": "2026届A班",
    "grade_level": "高一",
    "head_teacher_id": 5,
    "classroom_location": "教学楼101",
    "max_students": 40,
    "current_students": 35,
    "status": "active",
    "is_deleted": 0,
    "created_at": "2024-09-01T10:00:00",
    "updated_at": "2024-09-01T10:00:00"
}
```

### 18.2 分页查询班级信息

**接口地址**: `GET /classes/page`

**查询参数**:
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认10）
- `class_id` - 按班级ID精确查询
- `class_name` - 按班级名称模糊查询
- `grade_level` - 按年级筛选
- `head_teacher_id` - 按班主任ID筛选
- `status` - 按班级状态筛选 (active/graduated/disbanded)

**响应示例**:
```json
{
    "items": [
        {
            "class_id": 1,
            "class_name": "2026届A班",
            "grade_level": "高一",
            "head_teacher_id": 5,
            "classroom_location": "教学楼101",
            "max_students": 40,
            "current_students": 35,
            "status": "active",
            "is_deleted": 0,
            "created_at": "2024-09-01T10:00:00",
            "updated_at": "2024-09-01T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
}
```

### 18.3 更新班级信息

**接口地址**: `PUT /classes/{class_id}`

**请求体** (所有字段可选):
```json
{
    "head_teacher_id": 6,
    "current_students": 38
}
```

**响应示例**:
```json
{
    "class_id": 1,
    "class_name": "2026届A班",
    "grade_level": "高一",
    "head_teacher_id": 6,
    "classroom_location": "教学楼101",
    "max_students": 40,
    "current_students": 38,
    "status": "active",
    "is_deleted": 0,
    "created_at": "2024-09-01T10:00:00",
    "updated_at": "2024-09-15T14:00:00"
}
```

### 18.4 删除班级信息

**接口地址**: `DELETE /classes/{class_id}`

**响应示例**:
```json
{
    "code": 200,
    "msg": "删除成功"
}
```
