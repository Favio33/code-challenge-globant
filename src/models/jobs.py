from sqlalchemy import BigInteger, Column, DateTime, String, func

from database.db import Base


class Jobs(Base):

    __tablename__ = 'jobs'

    id = Column(BigInteger, primary_key=True)
    job = Column(String, nullable=False)
    last_updated = Column(DateTime, nullable=False, server_default=func.now())

    def __init__(self, job: str, id: int = None):
        self.job = job
        self.id = id

    def __repr__(self):
        return f"Job(id={self.id}, job={self.job}, last_updated={self.last_updated})"

    def to_dict(self):
        return {
            'id': self.id,
            'job': self.job
        }
