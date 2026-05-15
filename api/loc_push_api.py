from fastapi import APIRouter,Depends
from db.database import get_db
from service.loc_push_service import LOC_PUSH_Service
from sqlalchemy.orm import Session

router = APIRouter(tags=["地理位置获取与信息推送(润)"])

@router.get("/notifications")

def push_notifications(db: Session = Depends(get_db)):
    notifications=LOC_PUSH_Service.create(db)
    return notifications

