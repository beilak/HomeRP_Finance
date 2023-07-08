from sqlalchemy import String, Column, DateTime, func, Numeric, Integer
from sqlalchemy.orm import composite
from sqlalchemy_utils.types.currency import CurrencyType

from fin.adapters.db.db_conn import Base
from fin.models.common import Money


class TargetCnt(Base):
    __tablename__ = "target_cnt"
    target_cnt_id_type = Integer()
    target_cnt_id = Column(target_cnt_id_type, primary_key=True, autoincrement=True)
    unit_id = Column(String(32))
    name = Column(String(32))
    description = Column(String(128))
    value = Column(Numeric(precision=8))
    currency = Column(CurrencyType)
    init_value = Column(Numeric(precision=8))
    init_currency = Column(CurrencyType)
    user_login = Column(String(32))
    cr_date = Column(DateTime(timezone=True), server_default=func.now())
    upd_date = Column(DateTime(timezone=True), onupdate=func.now())

    target_money = composite(Money, value, currency)
    init_money = composite(Money, init_value, init_currency)


class TargetCntTemplate(Base):
    __tablename__ = "target_cnt_template"
    template_id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(32))
    description = Column(String(128))
    value = Column(Numeric(precision=8))
    currency = Column(CurrencyType)
    user_login = Column(String(32))
