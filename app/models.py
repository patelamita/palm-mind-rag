from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    file_type = Column(String, nullable=False)

    chunking_strategy = Column(String, nullable=False)

    number_of_chunks = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, nullable=False)

    interview_date = Column(String, nullable=False)

    interview_time = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )