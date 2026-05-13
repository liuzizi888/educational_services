"""
学生人脸识别API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.student_face_records import (
    StudentFaceRecordCreate,
    StudentFaceRecordUpdate,
    StudentFaceRecordResponse,
    StudentFaceRecordPageResponse
)
from service.student_face_records_service import StudentFaceRecordsService
from typing import Optional

router = APIRouter(tags=["学生人脸识别"])


@router.post("", response_model=StudentFaceRecordResponse)
def create(obj: StudentFaceRecordCreate, db: Session = Depends(get_db)):
    """创建学生人脸识别"""
    return StudentFaceRecordsService.create(db, obj)


@router.get("/page", response_model=StudentFaceRecordPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    face_id: Optional[int] = None,
    student_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """分页查询学生人脸识别
    - face_id: 按人脸记录ID精确查询
    - student_id: 按学生ID筛选
    """
    return StudentFaceRecordsService.get_page(db, page, page_size, face_id, student_id)


@router.put("/{face_id}", response_model=StudentFaceRecordResponse)
def update(face_id: int, obj: StudentFaceRecordUpdate, db: Session = Depends(get_db)):
    """更新学生人脸识别"""
    result = StudentFaceRecordsService.update(db, face_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="学生人脸识别不存在")
    return result


@router.delete("/{face_id}")
def delete(face_id: int, db: Session = Depends(get_db)):
    """删除学生人脸识别（软删除）"""
    success = StudentFaceRecordsService.delete(db, face_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生人脸识别不存在")
    return {"code": 200, "msg": "删除成功"}
