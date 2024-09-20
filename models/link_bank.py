from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
from database import Base
import enum


# Enum for Account Type
class AccountType(enum.Enum):
    CHECKING = "Checking"
    SAVINGS = "Savings"


class LinkBank(Base):
    __tablename__ = "link_banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Relation to countries
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    country = relationship("Country", back_populates="link_banks")




    # Relationship to User model
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="linked_banks")

    swift_code = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)  # Checking or Savings
    iban_number = Column(String, nullable=False)
    intermediary_bank_code = Column(String, nullable=True)  # Optional
    phone_number = Column(String, nullable=False)
    billing_address = Column(String, nullable=True)
    account_holder_name = Column(String, nullable=False)
    visibility = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=text('now()'))