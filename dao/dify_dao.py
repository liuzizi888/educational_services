from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import and_
from models.daily_reports import DailyReports
from typing import Optional, Tuple


class Dify_DAO:
    """对外数据访问"""

    @staticmethod
    def get_all(db: Session, sql_str: str):
        result = db.execute(text(sql_str))
        rows = result.fetchall()
        # 转换为可序列化的字典列表
        return [dict(row._mapping) for row in rows]
