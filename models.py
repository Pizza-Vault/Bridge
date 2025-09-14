from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
import datetime as dt

class Base(DeclarativeBase): pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64))
    timeslot: Mapped[str] = mapped_column(String(32))
    pickup_code: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(16))
    payment: Mapped[str] = mapped_column(String(16), default="not_paid")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)