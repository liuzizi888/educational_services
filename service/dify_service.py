from sqlalchemy.orm import Session
from dao.dify_dao import Dify_DAO


class DifyService:

    @staticmethod
    def get_all(db: Session, sql_all: str):
        return Dify_DAO.get_all(db, sql_all)
