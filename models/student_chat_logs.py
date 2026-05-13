"""
学生聊天记录模型
"""
from sqlalchemy import String, Integer, Text, Enum, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base
import enum


class RiskLevelEnum(str, enum.Enum):
    green = "green"
    yellow = "yellow"
    orange = "orange"
    red = "red"


class StudentChatLogs(Base):
    """学生聊天记录表"""
    __tablename__ = "t_student_chat_logs"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='日志ID')
    student_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment='学生ID（逻辑外键）')
    message_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='聊天内容')
    sentiment_score: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2), nullable=True, comment='情绪评分 (-1.0 到 1.0)')
    risk_level: Mapped[str] = mapped_column(String(20), default='green', comment='风险等级: green-绿色, yellow-黄色, orange-橙色, red-红色')
    keywords_detected: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='命中的敏感词')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudentChatLogs(log_id={self.log_id}, student_id={self.student_id}, risk_level={self.risk_level})>"
