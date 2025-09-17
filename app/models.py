from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
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
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    qty: Mapped[int] = mapped_column(Integer, default=0)
    warn_level: Mapped[int] = mapped_column(Integer, default=0)

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    provider: Mapped[str] = mapped_column(String(32), default="dummy")
    status: Mapped[str] = mapped_column(String(16), default="CAPTURED")
    amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
