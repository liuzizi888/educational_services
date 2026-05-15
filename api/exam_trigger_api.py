from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from service.exam_trigger_service import EXAM_TRIGGER_Service

router = APIRouter(tags=["未来30天考试信息获取与通知(润)"])

@router.get("/send_exam_notifications")
def send_exam_notification(db: Session = Depends(get_db)):
    result = EXAM_TRIGGER_Service.send(db)
    return result

