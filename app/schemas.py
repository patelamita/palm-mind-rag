from pydantic import BaseModel, EmailStr


class BookingRequest(BaseModel):
    name: str
    email: EmailStr
    interview_date: str
    interview_time: str