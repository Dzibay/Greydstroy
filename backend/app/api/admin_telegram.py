from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth import require_admin
from app.notify import (
    bot_info,
    delete_recipient,
    last_telegram_error,
    list_recipients,
    pending_chats,
    send_test,
    send_welcome,
    set_recipient_enabled,
    telegram_configured,
    upsert_recipient,
)
from app.config import settings

router = APIRouter(dependencies=[Depends(require_admin)])


class RecipientIn(BaseModel):
    chat_id: str = Field(min_length=1, max_length=32)
    name: str = Field(default="", max_length=120)
    username: str = Field(default="", max_length=64)


class EnabledIn(BaseModel):
    enabled: bool


@router.get("/admin/telegram")
def telegram_status() -> dict:
    info = bot_info()
    return {
        "configured": telegram_configured(),
        "bot": info,
        "reachable": bool(info.get("ok")),
        "error": info.get("error") or last_telegram_error(),
        "join_code": settings.telegram_join_code.strip(),
        "recipients": list_recipients(),
        "pending": pending_chats() if telegram_configured() and info.get("ok") else [],
    }


@router.post("/admin/telegram/recipients")
def add_recipient(body: RecipientIn) -> dict:
    try:
        rec = upsert_recipient(body.chat_id, body.name, body.username)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if telegram_configured():
        send_welcome(rec["chat_id"])
    return rec


@router.patch("/admin/telegram/recipients/{recipient_id}")
def toggle_recipient(recipient_id: int, body: EnabledIn) -> dict:
    try:
        set_recipient_enabled(recipient_id, body.enabled)
    except KeyError:
        raise HTTPException(status_code=404, detail="Получатель не найден")
    return {"ok": True, "id": recipient_id, "enabled": body.enabled}


@router.delete("/admin/telegram/recipients/{recipient_id}")
def remove_recipient(recipient_id: int) -> dict:
    try:
        delete_recipient(recipient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Получатель не найден")
    return {"ok": True, "id": recipient_id}


@router.post("/admin/telegram/test")
def test_telegram() -> dict:
    result = send_test()
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error") or "Не отправилось")
    return result
