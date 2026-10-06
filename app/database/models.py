from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(150)
    )

    phone: Mapped[str | None] = mapped_column(
        String(30)
    )

    address: Mapped[str | None] = mapped_column(
        String(300)
    )

    gstin: Mapped[str | None] = mapped_column(
        String(15)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="customer"
    )


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    invoice_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )

    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="invoices"
    )

    items: Mapped[list["InvoiceItem"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan"
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    invoice: Mapped["Invoice"] = relationship(
        back_populates="items"
    )
