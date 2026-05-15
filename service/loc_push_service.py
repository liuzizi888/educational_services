from sqlalchemy.orm import Session
from models import Students
import random
from datetime import datetime

LOCATION_TYPES = {
    1: "国内区域",
    2: "边境区域",
    3: "境外区域"
}

PROMPTS = {
    1: "安全性杠杠的!有困难找警察！",
    2: "你所在的区域近期治安事件较多，深夜请尽量避免独自出行！",
    3: "身处境外区域，务必注意防范危险！遇到危险时请及时联系当地大使馆！"
}
class LOC_PUSH_Service:
    @staticmethod
    def create(db: Session):
        result = db.query(Students.name).all()
        students = [row[0] for row in result]
        notifications = []
        for student in students:
            location_type = random.randint(1, 3)
            # 模拟定位信息 (1:国内, 2:边境, 3:境外)
            location_name = LOCATION_TYPES[location_type]
            prompt = PROMPTS[location_type]
            notifications.append([
                {"学生": f"{student}"},
                {"当前定位": f"{location_name}"},
                {"推送提示": f"{prompt}"},
                {"检测时间": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
            ])

        return notifications


