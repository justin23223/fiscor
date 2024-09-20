from sqlalchemy import Column, Integer, String, Enum, ForeignKey, TIMESTAMP, text, Float
from sqlalchemy.orm import relationship
from database import Base
import enum


# Enum for Account Type
class TransactionType(enum.Enum):
    INCOMING = "Incoming"
    OUTGOING = "Outgoing"


class TransactionType2(enum.Enum):
    WITHDRAW = "Withdraw"
    DEPOSIT = "Deposit"


class TransactionStatus(enum.Enum):
    PENDING = "Pending"
    DECLINED = "Declined"
    APPROVED = "Approved"
    VERIFYING = "VERIFYING"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    type = Column(Enum(TransactionType), default=TransactionType.INCOMING)
    typ2 = Column(Enum(TransactionType2), default=TransactionType2.WITHDRAW)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    amount = Column(Float)
    currency = Column(String)
    currency_symbol = Column(String(10), nullable=False)

    # Foreign key to User model
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to User model
    user = relationship("User", back_populates="transactions")

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=text('now()'))
