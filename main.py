from fastapi import FastAPI, HTTPException, Request
import uvicorn
from log.log import logger
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.auth_middleware import AuthMiddleware
from dotenv import load_dotenv
import os
from api.user_permissions_api import router as user_permissions_router
from api.employees_api import router as employees_router
from api.clients_api import router as clients_router
from api.global_study_policies_api import router as global_study_policies_router
from api.study_agency_info_api import router as study_agency_info_router
from api.training_courses_api import router as training_courses_router
from api.activity_info_api import router as activity_info_router
from api.activity_bookings_api import router as activity_bookings_router
from api.faq_api import router as faq_router
from api.sales_results_api import router as sales_results_router
from api.daily_reports_api import router as daily_reports_router
from api.monthly_goals_api import router as monthly_goals_router
from api.students_api import router as students_router
from api.student_face_records_api import router as student_face_records_router
from api.student_leaves_api import router as student_leaves_router
from api.student_complaints_api import router as student_complaints_router
from api.student_chat_logs_api import router as student_chat_logs_router
from api.student_photos_api import router as student_photos_router
from api.exams_api import router as exams_router
from api.student_grades_api import router as student_grades_router
from api.knowledge_base_overseas_api import router as knowledge_base_overseas_router
from api.classes_api import router as classes_router
from api.dify_api import router as dify_router
from api.loc_push_api import router as loc_push_router
from api.face_emotion_api import router as face_emotion_router
from api.exam_trigger_api import router as exam_trigger_router

load_dotenv()

# 从环境变量读取配置
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8888'))
FRONTEND_DIR = os.getenv('FRONTEND_DIR', 'frontend')
LOG_DIR = os.getenv('LOG_DIR', 'log')

app = FastAPI(title="教育服务",
              description="基于 FastAPI + RAG + Agent + NL2SQL + SQLAlchemy 实现的智能教育服务",
              version="1.0.0"
              )

# 注册认证中间件
app.add_middleware(AuthMiddleware)

# 注册路由
app.include_router(user_permissions_router, prefix="/user_permissions")
app.include_router(employees_router, prefix="/employees")
app.include_router(clients_router, prefix="/clients")
app.include_router(global_study_policies_router, prefix="/global_study_policies")
app.include_router(study_agency_info_router, prefix="/study_agency_info")
app.include_router(training_courses_router, prefix="/training_courses")
app.include_router(activity_info_router, prefix="/activity_info")
app.include_router(activity_bookings_router, prefix="/activity_bookings")
app.include_router(faq_router, prefix="/faq")
app.include_router(sales_results_router, prefix="/sales_results")
app.include_router(daily_reports_router, prefix="/daily_reports")
app.include_router(monthly_goals_router, prefix="/monthly_goals")
app.include_router(students_router, prefix="/students")
app.include_router(student_face_records_router, prefix="/student_face_records")
app.include_router(student_leaves_router, prefix="/student_leaves")
app.include_router(student_complaints_router, prefix="/student_complaints")
app.include_router(student_chat_logs_router, prefix="/student_chat_logs")
app.include_router(student_photos_router, prefix="/student_photos")
app.include_router(exams_router, prefix="/exams")
app.include_router(student_grades_router, prefix="/student_grades")
app.include_router(knowledge_base_overseas_router, prefix="/knowledge_base_overseas")
app.include_router(classes_router, prefix="/classes")
app.include_router(dify_router, prefix="/dify")
app.include_router(loc_push_router, prefix="/loc_push")
app.include_router(face_emotion_router, prefix="/face_emotion")
app.include_router(exam_trigger_router, prefix="/exam_trigger")


#用来查看日志
app.mount("/log", StaticFiles(directory=LOG_DIR))

#挂载 frontend 文件夹
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# 根路径重定向到登录页面
from fastapi.responses import RedirectResponse

@app.get("/", response_class=RedirectResponse, tags=['登录页面'])
def root():
    # 重定向到登录页面
    return "/frontend/login.html"

# 登录页面
@app.get("/login", response_class=HTMLResponse, tags=['登录页面'])
def login_page():
    try:
        with open("frontend/login.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # 如果前端文件不存在，返回简单的登录页面
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>教育服务系统</title>
            <style>
                body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; }
                .login-container { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 350px; }
                h1 { text-align: center; color: #333; margin-bottom: 30px; }
                .form-group { margin-bottom: 20px; }
                label { display: block; margin-bottom: 5px; color: #666; }
                input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                button { width: 100%; padding: 12px; background: #1890ff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                button:hover { background: #40a9ff; }
                .message { margin-top: 15px; padding: 10px; border-radius: 4px; display: none; }
                .error { background: #fff2f0; color: #ff4d4f; border: 1px solid #ffccc7; }
                .success { background: #f6ffed; color: #52c41a; border: 1px solid #b7eb8f; }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h1>教育服务系统</h1>
                <form id="loginForm">
                    <div class="form-group">
                        <label>用户名</label>
                        <input type="text" id="username" required>
                    </div>
                    <div class="form-group">
                        <label>密码</label>
                        <input type="password" id="password" required>
                    </div>
                    <button type="submit">登录</button>
                    <div id="message" class="message"></div>
                </form>
            </div>
            <script>
                document.getElementById('loginForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    const messageDiv = document.getElementById('message');
                    
                    try {
                        const response = await fetch('/user_permissions/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ username, password })
                        });
                        
                        const data = await response.json();
                        
                        if (response.ok) {
                            messageDiv.className = 'message success';
                            messageDiv.textContent = '登录成功！Token: ' + data.token.substring(0, 50) + '...';
                            messageDiv.style.display = 'block';
                            localStorage.setItem('token', data.token);
                        } else {
                            messageDiv.className = 'message error';
                            messageDiv.textContent = data.detail || '登录失败';
                            messageDiv.style.display = 'block';
                        }
                    } catch (error) {
                        messageDiv.className = 'message error';
                        messageDiv.textContent = '请求失败: ' + error.message;
                        messageDiv.style.display = 'block';
                    }
                });
            </script>
        </body>
        </html>
        """


if __name__ == '__main__':
    logger.info(f'启动项目，监听地址：http://{HOST}:{PORT}')
    uvicorn.run('main:app', host=HOST, port=PORT)
