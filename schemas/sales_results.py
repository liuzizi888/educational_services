"""
销售成果Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class SalesResultBase(BaseModel):
    """销售成果基础Schema"""
    employee_id: int = Field(..., description='员工ID')
    client_id: Optional[int] = Field(None, description='客户ID')
    contract_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description='签约金额')
    contract_date: Optional[date] = Field(None, description='签约日期')
    product_type: Optional[str] = Field(None, max_length=50, description='产品类型')


class SalesResultCreate(SalesResultBase):
    """创建销售成果Schema"""
    pass


class SalesResultUpdate(BaseModel):
    """更新销售成果Schema"""
    employee_id: Optional[int] = Field(None, description='员工ID')
    client_id: Optional[int] = Field(None, description='客户ID')
    contract_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description='签约金额')
    contract_date: Optional[date] = Field(None, description='签约日期')
    product_type: Optional[str] = Field(None, max_length=50, description='产品类型')


class SalesResultResponse(BaseModel):
    """销售成果响应Schema"""
    result_id: int
    employee_id: int
    client_id: Optional[int] = None
    contract_amount: Optional[Decimal] = None
    contract_date: Optional[date] = None
    product_type: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SalesResultPageResponse(BaseModel):
    """销售成果分页响应Schema"""
    items: list[SalesResultResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
