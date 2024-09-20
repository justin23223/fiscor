from sqlalchemy import Column, Integer
from database import Base



class CaseStatistics(Base):
    __tablename__ = "case_statistic"

    id = Column(Integer, primary_key=True, index=True)
    successful_cases = Column(Integer)
    closed_cased = Column(Integer)
    trusted_clients = Column(Integer)
    expert_teams = Column(Integer)



