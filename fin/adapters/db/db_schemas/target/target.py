from sqlalchemy import Column, ForeignKey, DateTime, func, Numeric, Integer, String
from sqlalchemy.orm import composite
from sqlalchemy_utils.types.currency import CurrencyType

from fin.adapters.db.db_conn import Base
from fin.adapters.db.db_schemas.target.target_cnt import TargetCnt
from fin.models.common import Money


class Target(Base):
    __tablename__ = "target"
    target_id_type = Integer()
    target_id = Column(target_id_type, primary_key=True, autoincrement=True)
    target_cnt_id = Column(TargetCnt.target_cnt_id_type,
                           ForeignKey(TargetCnt.target_cnt_id))
    user_login = Column(String(32))
    value = Column(Numeric(precision=8))
    currency = Column(CurrencyType)
    cr_date = Column(DateTime(timezone=True), server_default=func.now())
    upd_date = Column(DateTime(timezone=True), onupdate=func.now())

    target_money = composite(Money, value, currency)
