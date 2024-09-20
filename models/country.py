from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)

    # Reference to LinkBank
    link_banks = relationship("LinkBank", back_populates="country")  # Changed to 'link_banks'
    # Add this relationship to link users with the country
    users = relationship("User", back_populates="country")
    def __str__(self):
        return self.name
