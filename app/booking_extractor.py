import re

from app.llm import generate_response


def extract_booking_details(message: str) -> dict:
    """Extract interview booking details from a user message."""

    prompt = f"""
Extract the interview booking details from this message.

Return exactly these four lines:
Name: ...
Email: ...
Date: ...
Time: ...

If a value is missing, write None.

Message:
{message}
"""

    response = generate_response(prompt)

    details = {
        "name": None,
        "email": None,
        "interview_date": None,
        "interview_time": None,
    }

    name_match = re.search(
        r"Name:\s*(.+)",
        response,
        re.IGNORECASE,
    )

    email_match = re.search(
        r"Email:\s*(.+)",
        response,
        re.IGNORECASE,
    )

    date_match = re.search(
        r"Date:\s*(.+)",
        response,
        re.IGNORECASE,
    )

    time_match = re.search(
        r"Time:\s*(.+)",
        response,
        re.IGNORECASE,
    )

    if name_match:
        details["name"] = name_match.group(1).strip()

    if email_match:
        details["email"] = email_match.group(1).strip()

    if date_match:
        details["interview_date"] = date_match.group(1).strip()

    if time_match:
        details["interview_time"] = time_match.group(1).strip()

    return details