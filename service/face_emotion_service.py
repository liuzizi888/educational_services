from sqlalchemy.orm import Session
import dashscope
from pydantic import BaseModel
from typing import Optional
import pymysql
import os
import random
import datetime
# ================= 配置区域 =================

DASHSCOPE_API_KEY = "sk-5acebcdae5ec4da9ad1cc8a129d90278"
dashscope.api_key = DASHSCOPE_API_KEY

BASE_DIR = 'pic/reg_pic'
FACE_DIR = 'pic/face_pic'
DEVICE_IDS = ['CAM-001', 'CAM-002', 'CAM-003']

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'educational_services_deepseek',
    'charset': 'utf8mb4'
}

# ==========================================

# 请求体模型
class AnalysisRequest(BaseModel):
    student_name: str

# 响应体模型
class AnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

def get_student_info(student_name):
    """从数据库获取学生ID"""
    conn = cursor = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "SELECT student_id FROM t_students WHERE name = %s"
        cursor.execute(sql, (student_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"查询学生信息失败：{e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_emotion_analysis(image1_path, image2_path):
    """调用大模型分析"""
    try:
        file_url_1 = f"file://{os.path.abspath(image1_path)}"
        file_url_2 = f"file://{os.path.abspath(image2_path)}"

        prompt = (
            "你是一名专业的心理医生。以第一张图为基准，对比第二张图面部表情的变化。"
            "给出：情绪标签(green/yellow/red)，情绪分数(0-1)，具体情绪(英文)。"
            "最后只返回格式如：(green,0.11,happy)"
            "更多示例：(green,0.05,calm),(green,0.1,happy),(yellow,0.7,depress),(red,0.9,angry),"
        )

        messages = [{
            "role": "user",
            "content": [
                {"image": file_url_1},
                {"image": file_url_2},
                {"text": prompt}
            ]
        }]

        response = dashscope.MultiModalConversation.call(model='qwen3-vl-plus', messages=messages)

        if response.status_code == 200:  # HTTPStatus.OK
            return response.output.choices[0].message.content[0]['text'].strip()
        else:
            return f"(Error, 0.0, {response.status_code})"

    except Exception as e:
        print(f"发生未知异常：{e}")
        return f"(Error, 0.0, Exception)"

def save_to_database(data_tuple):
    conn = cursor = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """
        INSERT INTO t_student_photos 
        (student_id, risk_level, sentiment_score, mood_status, device_id, created_at, photo_url) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, data_tuple)
        conn.commit()
        return True
    except Exception as e:
        print(f"数据库插入失败：{e}")
        if conn: conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


class FACE_EMOTION_Service:
    @staticmethod
    def push(request: AnalysisRequest,db: Session):
        student_name = request.student_name.strip()

        # 1. 获取学生ID
        student_id = get_student_info(student_name)

        # 2. 确定图片路径
        base_folder = os.path.join(BASE_DIR, student_name)
        face_folder = os.path.join(FACE_DIR, student_name)
        base_img_path = os.path.join(base_folder, 'c.png')

        # 3. 随机抽取打卡图
        png_files = [f for f in os.listdir(face_folder) if f.lower().endswith('.png')]


        random_face_img = random.choice(png_files)
        face_img_path = os.path.join(face_folder, random_face_img)

        # 4. 调用大模型分析
        emotion_result = get_emotion_analysis(base_img_path, face_img_path)

        # 5. 解析结果并保存
        emotion_parts = emotion_result.strip('()').split(',')
        if len(emotion_parts) == 3:
            risk_level, sentiment_score, mood_status = emotion_parts
        else:
            risk_level, sentiment_score, mood_status = "unknown", "0.0", "unknown"

        random_device = random.choice(DEVICE_IDS)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        abs_image_path = os.path.abspath(face_img_path)

        final_data = (
            student_id, risk_level, sentiment_score,
            mood_status, random_device, current_time, abs_image_path
        )

        save_success = save_to_database(final_data)

        # 6. 构造返回结果
        return AnalysisResponse(
            success=True,
            message="分析成功",
            data={
                "student_name": student_name,
                "student_id": student_id,
                "emotion_result": emotion_result,
                "risk_level": risk_level,
                "sentiment_score": sentiment_score,
                "mood_status": mood_status,
                "device_id": random_device,
                "timestamp": current_time,
                "photo_path": abs_image_path,
                "database_saved": save_success
            }
        )