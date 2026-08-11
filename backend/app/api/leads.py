from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.db import pool

router = APIRouter()


class LeadIn(BaseModel):
    name: str = Field(default="", max_length=200)
    phone: str = Field(min_length=10, max_length=32)
    drawing: str = Field(default="yes", pattern="^(yes|no)$")
    comment: str = Field(default="", max_length=4000)
    file_name: str = Field(default="", max_length=300)
    source: str = Field(default="", max_length=300)


@router.post("/leads")
def create_lead(lead: LeadIn) -> dict:
    if not lead.phone.strip():
        raise HTTPException(status_code=422, detail="Телефон обязателен")
    with pool.connection() as conn:
        row = conn.execute(
            """
            INSERT INTO leads (name, phone, has_drawing, comment, file_name, source)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                lead.name.strip(),
                lead.phone.strip(),
                lead.drawing == "yes",
                lead.comment.strip(),
                lead.file_name.strip(),
                lead.source.strip(),
            ),
        ).fetchone()
    return {"ok": True, "id": row[0]}
