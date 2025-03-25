from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, func

from database.db import Base


class HiredEmployees(Base):

    __tablename__ = 'hired_employees'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=True)
    datetime = Column(DateTime, nullable=True)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id"), nullable=True)
    last_updated = Column(DateTime, nullable=False, server_default=func.now())

    def __init__(self, name: str, datetime: str, department_id: int, job_id: int, id: int = None):
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id
        self.id = id

    def __repr__(self):
        return f"""Department(id={self.id}, name={self.name}, datetime={self.datetime},
            department_id={self.department_id}, job_id={self.job_id}, last_updated={self.last_updated})"""  # noqa: E501

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'datetime': self.datetime,
            'department_id': self.department_id,
            'job_id': self.job_id
        }
