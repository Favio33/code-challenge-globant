from sqlalchemy import BigInteger, Column, DateTime, String, func

from database.db import Base


class Department(Base):

    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True)
    department = Column(String, nullable=False)
    last_updated = Column(DateTime, nullable=False, server_default=func.now())

    def __init__(self, department: str, id: int = None):
        self.department = department
        self.id = id

    def __repr__(self):
        return f"Department(id={self.id}, departments={self.department}, last_updated={self.last_updated})"  # noqa: E501

    def to_dict(self):
        return {
            'id': self.id,
            'department': self.department
        }
