from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BankCard(Base):
    __tablename__ = "bank_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    cardholder_name = Column(String, nullable=False)
    expiration_date = Column(String, nullable=False)
    cvv = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="bank_cards")