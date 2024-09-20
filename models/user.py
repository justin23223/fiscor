from sqlalchemy import Column, Integer, String, Boolean, Enum, Float, Text, TIMESTAMP, text, ForeignKey
from database import Base
import enum
from sqlalchemy.orm import relationship


# Enum for the verification status
class VerificationStatus(enum.Enum):
    UNVERIFIED = "Unverified"
    VERIFIED = "Verified"


# Enum for the user role system
class RoleSystem(enum.Enum):
    ADMIN = "Admin"
    USER = "User"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    currency = Column(String)
    currency_symbol = Column(String(10), nullable=False)

    role_system = Column(Enum(RoleSystem), nullable=False, server_default="USER")  # Default role is USER

    verification_status = Column(Enum(VerificationStatus), nullable=False, server_default="UNVERIFIED")

    reference_number = Column(String, unique=True, nullable=False)

    stolen_funds = Column(Float, default=0.0)
    recovered_funds = Column(Float, default=0.0)

    complain_text = Column(Text, nullable=True)
    wallet_address = Column(String, unique=True, nullable=True)
    wallet_address_blockchain = Column(String, nullable=True)

    note = Column(Text, nullable=True)  # For internal comments

    whitelisted = Column(Boolean, default=False)
    required_amount_for_whitelist = Column(Float, default=0.0)

    total_withdrawable_balance = Column(Float, default=0.0)
    # Add the country_id as a ForeignKey and relationship
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", back_populates="users")  # Define the relationship with Country

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=text('now()'))
    bank_cards = relationship("BankCard", back_populates="user")
    linked_banks = relationship("LinkBank", back_populates="user")

    # Relationship to Transaction model
    transactions = relationship("Transaction", back_populates="user")

    def __str__(self):
        return self.username
