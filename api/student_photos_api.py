"""
学生人脸识别与心情预判API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.student_photos import (
    StudentPhotoCreate,
    StudentPhotoUpdate,
    StudentPhotoResponse,
    StudentPhotoPageResponse
)
from service.student_photos_service import StudentPhotosService
from typing import Optional

router = APIRouter(tags=["学生人脸识别"])


@router.post("", response_model=StudentPhotoResponse)
def create(obj: StudentPhotoCreate, db: Session = Depends(get_db)):
    """创建学生人脸识别记录"""
    return StudentPhotosService.create(db, obj)


@router.get("/page", response_model=StudentPhotoPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    photo_id: Optional[int] = None,
    student_id: Optional[int] = None,
    mood_status: Optional[str] = None,
    risk_level: Optional[str] = None,
    capture_scene: Optional[str] = None,
    device_id: Optional[str] = None,
    sentiment_min: Optional[float] = None,
    sentiment_max: Optional[float] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生人脸识别记录
    - photo_id: 按记录ID精确查询
    - student_id: 按学生ID筛选
    - mood_status: 按心情状态筛选（开心、平静、焦虑、愤怒、悲伤）
    - risk_level: 按风险等级筛选 (green/yellow/orange/red)
    - capture_scene: 按抓拍场景模糊查询
    - device_id: 按设备编号筛选
    - sentiment_min: 按情绪评分最小值筛选
    - sentiment_max: 按情绪评分最大值筛选
    - created_at_start: 按识别时间起筛选 (格式: YYYY-MM-DD HH:MM:SS)
    - created_at_end: 按识别时间止筛选 (格式: YYYY-MM-DD HH:MM:SS)
    """
    return StudentPhotosService.get_page(
        db, page, page_size, photo_id, student_id, mood_status, risk_level,
        capture_scene, device_id, sentiment_min, sentiment_max,
        created_at_start, created_at_end
    )


@router.put("/{photo_id}", response_model=StudentPhotoResponse)
def update(photo_id: int, obj: StudentPhotoUpdate, db: Session = Depends(get_db)):
    """更新学生人脸识别记录"""
    result = StudentPhotosService.update(db, photo_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生人脸识别记录不存在")
    return result


@router.delete("/{photo_id}")
def delete(photo_id: int, db: Session = Depends(get_db)):
    """删除学生人脸识别记录（软删除）"""
    success = StudentPhotosService.delete(db, photo_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生人脸识别记录不存在")
    return {"code": 200, "msg": "删除成功"}
