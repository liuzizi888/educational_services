import yagmail
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from datetime import datetime
import time
import pymysql


# ================= 配置区域 =================

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'educational_services_deepseek',
    'charset': 'utf8mb4'
}

# 邮箱配置
EMAIL_USER = '2027015069@qq.com'
EMAIL_PASSWORD = 'cvbuzghfhulabhji'

# ==========================================

class EXAM_TRIGGER_Service:
    @staticmethod
    def send(db: Session):
        conn = None
        cursor = None
        try:
            # 1. 连接数据库
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # 2. 编写关联查询 SQL (加入了考试地点 exam_location)
            target_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            today = datetime.now().strftime('%Y-%m-%d')

            sql = """
                SELECT 
                    s.name AS student_name, 
                    s.email AS student_email, 
                    e.exam_time, 
                    e.class_name,
                    e.location 
                FROM t_exams e
                JOIN t_classes c ON e.class_name = c.class_name
                JOIN t_students s ON c.class_id = s.class_id
                WHERE e.exam_time >= %s AND e.exam_time <= %s
            """

            cursor.execute(sql, (today, target_date))
            exam_list = cursor.fetchall()

            # 3. 初始化邮件客户端
            yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD, host='smtp.qq.com', port=465)

            notifications = []  # 用于收集发送结果

            # 4. 遍历查询结果并发送邮件
            if exam_list:
                print(f"发现 {len(exam_list)} 条待发送的考试通知。")
                for student in exam_list:
                    # 解包时多接收一个 exam_location
                    student_name, student_email, exam_time, class_name, location = student
                    exam_time_str = exam_time.strftime('%Y年%m月%d日 %H:%M')

                    # 邮件内容中加入了考试地点
                    subject = f"【考试提醒】{class_name} 近期考试安排"
                    contents = f"""
                    亲爱的 {student_name} 同学：

                    您好！温馨提醒您，您所在的班级 ({class_name}) 即将迎来考试。

                    考试时间：{exam_time_str}
                    考试地点：{location}

                    请提前做好准备，按时参加考试。祝您取得优异成绩！
                    """

                    try:
                        # 发送邮件
                        yag.send(to=student_email, subject=subject, contents=contents)
                        print(f"成功发送邮件至: {student_email} ({student_name})")
                        # 记录成功信息
                        notifications.append({
                            "status": "success",
                            "student_name": student_name,
                            "student_email": student_email,
                            "class_name": class_name,
                            "exam_time": exam_time_str,
                            "location": location,
                            "message": "邮件发送成功"
                        })
                    except Exception as e:
                        error_msg = f"发送邮件失败: {str(e)}"
                        print(error_msg)
                        # 记录失败信息
                        notifications.append({
                            "status": "failed",
                            "student_name": student_name,
                            "student_email": student_email,
                            "class_name": class_name,
                            "exam_time": exam_time_str,
                            "location": location,
                            "message": error_msg
                        })
                    # 避免发送过快被限制，暂停 1 秒
                    time.sleep(1)
            else:
                return {"notifications": [], "message": "近期暂无考试安排，无需发送通知"}

            return {"notifications": notifications, "message": f"共处理 {len(notifications)} 条通知"}

        except Exception as e:
            error_msg = f"数据库查询或处理出错: {str(e)}"
            print(error_msg)
            return {"notifications": [], "message": error_msg, "status": "error"}

        finally:
            # 5. 关闭数据库连接
            if cursor:
                cursor.close()
            if conn:
                conn.close()



