from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from service.dify_service import DifyService

router = APIRouter(tags=["dify_调用sql通用接口"])


@router.get("/")
def get_all(query_sql: str, db: Session = Depends(get_db)):
    return DifyService.get_all(db, query_sql)
