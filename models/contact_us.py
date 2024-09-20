from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from database import Base


class ContactUs(Base):
    __tablename__ = "contact_us"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)  # Phone number is optional
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    def __repr__(self):
        return f"<ContactUs(name={self.name}, email={self.email}, subject={self.subject})>"
