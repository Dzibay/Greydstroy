import time

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.auth import check_password, make_token, require_admin
from app.db import pool

router = APIRouter()


class LoginIn(BaseModel):
    password: str


@router.post("/admin/login")
def login(body: LoginIn) -> dict:
    if not check_password(body.password):
        time.sleep(0.7)  # притормаживаем перебор пароля
        raise HTTPException(status_code=401, detail="Неверный пароль")
    return {"token": make_token()}


@router.get("/admin/leads", dependencies=[Depends(require_admin)])
def list_leads(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> dict:
    with pool.connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        rows = conn.execute(
            """
            SELECT id, name, phone, has_drawing, comment, file_name, source, created_at
            FROM leads
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        ).fetchall()
    items = [
        {
            "id": r[0],
            "name": r[1],
            "phone": r[2],
            "has_drawing": r[3],
            "comment": r[4],
            "file_name": r[5],
            "source": r[6],
            "created_at": r[7].isoformat(),
        }
        for r in rows
    ]
    return {"total": total, "items": items}
