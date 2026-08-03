from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

if TYPE_CHECKING:
    from src.models.payment_method import PaymentMethod
    from src.models.reservation import Reservation
    from src.models.room import Room
    from src.models.user import User


"""
Declarar Modelo de Base de DeclarativeBase
Clase de Herencia para los modelos de SQLAlchemy.
"""
class Base(DeclarativeBase):
    pass

"""
Modelo de Lodging:
- lodging_id: Integer, Primary Key, Autoincrement, Index
- initial_time: DateTime(timezone=True), Not Null
- final_time: DateTime(timezone=True), Not Null
- stay_type: String(50), Not Null
- comments: String(250), Nullable
- room_id: Integer, Not Null, Foreign Key to rooms.room_id
- user_id: Integer, Not Null, Foreign Key to users.user_id
- payment_id: Integer, Not Null, Foreign Key to payment_methods.payment_id
- reservation_id: Integer, Nullable, Foreign Key to reservations.reservation_id
- room: Relationship with Room
- user: Relationship with User
- payment_method: Relationship with PaymentMethod
- reservation: Relationship with Reservation
- __table_args__: Restricciones CHECK
"""
class Lodging(Base):
    __tablename__ = "lodgings"

    # Atributos Propios de la tabla
    lodging_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    initial_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    final_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    stay_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    comments: Mapped[Optional[str]] = mapped_column(
        String(250), 
        nullable=True
    )

    # Llaves Foraneas
    # Relacion con Room
    room_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rooms.room_id", 
            ondelete="RESTRICT", 
            onupdate="CASCADE"
        ),
        nullable=False,
        index=True,
    )
    # Relacion con User
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.user_id", 
            ondelete="RESTRICT", 
            onupdate="CASCADE"
        ),
        nullable=False,
        index=True,
    )
    # Relacion con PaymentMethod
    payment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "payment_methods.payment_id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    # Relacion con Reservation
    reservation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "reservations.reservation_id",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    # Relaciones ORM
    # Relacion con Room
    room: Mapped["Room"] = relationship(
        "Room", 
        back_populates="lodgings"
    )
    # Relacion con User
    user: Mapped["User"] = relationship(
        "User", 
        back_populates="lodgings"
    )
    # Relacion con PaymentMethod
    payment_method: Mapped["PaymentMethod"] = relationship(
        "PaymentMethod", 
        back_populates="lodgings"
    )
    # Relacion con Reservation
    reservation: Mapped[Optional["Reservation"]] = relationship(
        "Reservation", 
        back_populates="lodgings"
    )

    # Restricciones CHECK
    __table_args__ = (
        CheckConstraint(
            "final_time > initial_time", name="chk_lodgings_chronology"
        ),
        CheckConstraint(
            "stay_type IN ('3 horas', '4 horas', '5 horas', '6 horas', 'amanecer')",
            name="chk_lodgings_stay_type",
        ),
    )