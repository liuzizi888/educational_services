from fastapi import APIRouter,Depends
from service.face_emotion_service import AnalysisRequest
from sqlalchemy.orm import Session
from db.database import get_db
from service.face_emotion_service import FACE_EMOTION_Service

router = APIRouter(tags=["人脸识别打卡与情绪分析(润)"])

@router.post("/analyze")
def start_analysis(request: AnalysisRequest,db: Session = Depends(get_db)):
    result=FACE_EMOTION_Service.push(request,db)
    return result


