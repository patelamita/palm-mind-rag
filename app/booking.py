from sqlalchemy.orm import Session

from app.models import Booking


def create_booking(
    db: Session,
    name: str,
    email: str,
    interview_date: str,
    interview_time: str,
) -> Booking:
    """Create and store an interview booking."""

    booking = Booking(
        name=name,
        email=email,
        interview_date=interview_date,
        interview_time=interview_time,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking