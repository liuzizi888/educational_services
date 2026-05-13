"""
销售成果模型
"""
from sqlalchemy import String, Integer, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from db.database import Base


class SalesResults(Base):
    """销售成果表"""
    __tablename__ = "t_sales_results"
    
    result_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='员工ID')
    client_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='客户ID')
    contract_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment='签约金额')
    contract_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='签约日期')
    product_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='产品类型')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<SalesResults(result_id={self.result_id}, employee_id={self.employee_id}, contract_amount={self.contract_amount})>"
