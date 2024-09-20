# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base
#
#
#
#
# class Bank(Base):
#     __tablename__ = "banks"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False, unique=True)
#
#     country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
#
#     # Reference to country
#     country = relationship("Country", back_populates="banks")
#     linked_banks = relationship("LinkBank", back_populates="bank")
#
#     def __str__(self):
#         return self.name