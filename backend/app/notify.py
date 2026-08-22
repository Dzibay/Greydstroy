"""Уведомления о заявках через Telegram Bot API.

Бот — курьер, не чат с клиентами. Получатели живут в telegram_recipients
плюс TELEGRAM_CHAT_ID из .env. Отправка в фоне и не ломает форму.
"""

from __future__ import annotations

import json
import logging
import mimetypes
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.config import settings
from app.db import pool
from app.paths import UPLOAD_DIR

log = logging.getLogger("app.notify")

PAGE_NAMES = {
    "/": "Главная",
    "/kalkulyator": "Калькулятор",
    "/uslugi": "Услуги",
    "/metallokonstruktsii": "Металлоконструкции",
    "/projects": "Объекты",
    "/kontakty": "Контакты",
    "/dostavka": "Доставка",
    "/rekvizity": "Реквизиты",
}
TG_FILE_LIMIT = 45 * 1024 * 1024
_last_error = ""


def last_telegram_error() -> str:
    return _last_error


def _api_base() -> str:
    return (settings.telegram_api_base or "https://api.telegram.org").strip().rstrip("/")


def _opener() -> urllib.request.OpenerDirector:
    proxy = settings.telegram_proxy.strip()
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    return urllib.request.build_opener(*handlers)


def _esc(value: str) -> str:
    return (
        (value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _page_label(path: str) -> str:
    clean = (path or "").split("?")[0] or "/"
    if clean in PAGE_NAMES:
        return PAGE_NAMES[clean]
    if clean.startswith("/uslugi/"):
        return f"Услуга · {clean[8:]}"
    if clean.startswith("/projects/"):
        return f"Объект · {clean[10:]}"
    return path or "—"


def international_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if not digits:
        return ""
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    if digits.startswith("7") and len(digits) >= 11:
        return "+" + digits[:11]
    return "+" + digits if not (phone or "").startswith("+") else phone.strip()


def pretty_phone(phone: str) -> str:
    intl = international_phone(phone)
    digits = re.sub(r"\D", "", intl)
    if len(digits) == 11 and digits.startswith("7"):
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return intl or phone


def telegram_configured() -> bool:
    return bool(settings.telegram_bot_token.strip())


def telegram_api(method: str, payload: dict | None = None, file: Path | None = None) -> dict:
    global _last_error
    token = settings.telegram_bot_token.strip()
    if not token:
        return {}
    url = f"{_api_base()}/bot{token}/{method}"
    try:
        if file and file.is_file():
            data, headers = _multipart(payload or {}, file)
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        else:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload or {}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
        with _opener().open(req, timeout=20) as resp:
            _last_error = ""
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        _last_error = f"HTTP {exc.code}: {detail[:180]}"
        log.warning("Telegram %s HTTP %s: %s", method, exc.code, detail)
        try:
            return json.loads(detail)
        except json.JSONDecodeError:
            return {"ok": False, "description": detail}
    except Exception as exc:
        _last_error = str(exc.reason if getattr(exc, "reason", None) else exc)
        log.warning("Telegram %s не удался: %s", method, _last_error)
        return {"ok": False, "description": _last_error}


def _multipart(fields: dict[str, Any], file: Path) -> tuple[bytes, dict[str, str]]:
    boundary = uuid4().hex
    chunks: list[bytes] = []
    for key, value in fields.items():
        if value is None:
            continue
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        chunks.append(f"{value}\r\n".encode())
    mime = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
    chunks.append(f"--{boundary}\r\n".encode())
    chunks.append(
        f'Content-Disposition: form-data; name="document"; filename="{file.name}"\r\n'.encode()
    )
    chunks.append(f"Content-Type: {mime}\r\n\r\n".encode())
    chunks.append(file.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), {"Content-Type": f"multipart/form-data; boundary={boundary}"}


def bot_info() -> dict:
    if not telegram_configured():
        return {"ok": False, "configured": False}
    data = telegram_api("getMe")
    result = data.get("result") or {}
    return {
        "ok": bool(data.get("ok")),
        "configured": True,
        "username": result.get("username") or "",
        "name": result.get("first_name") or "",
        "id": result.get("id"),
        "error": "" if data.get("ok") else (data.get("description") or last_telegram_error() or "нет ответа от Telegram"),
        "api_base": _api_base(),
        "via_proxy": bool(settings.telegram_proxy.strip()),
    }


def list_recipients() -> list[dict]:
    _seed_env_recipients()
    with pool.connection() as conn:
        rows = conn.execute(
            """
            SELECT id, chat_id, name, username, enabled, created_at
            FROM telegram_recipients
            ORDER BY created_at
            """,
        ).fetchall()
    return [
        {
            "id": r[0],
            "chat_id": r[1],
            "name": r[2],
            "username": r[3],
            "enabled": r[4],
            "created_at": r[5].isoformat(),
            "from_env": False,
        }
        for r in rows
    ]


def _seed_env_recipients() -> None:
    raw = settings.telegram_chat_id
    ids = [part.strip() for part in raw.split(",") if part.strip()]
    if not ids:
        return
    with pool.connection() as conn:
        for chat_id in ids:
            conn.execute(
                """
                INSERT INTO telegram_recipients (chat_id, name)
                VALUES (%s, 'из .env')
                ON CONFLICT (chat_id) DO NOTHING
                """,
                (chat_id,),
            )


def enabled_chat_ids() -> list[str]:
    _seed_env_recipients()
    with pool.connection() as conn:
        rows = conn.execute(
            "SELECT chat_id FROM telegram_recipients WHERE enabled = TRUE",
        ).fetchall()
    return [r[0] for r in rows]


def upsert_recipient(chat_id: str, name: str = "", username: str = "") -> dict:
    chat_id = str(chat_id).strip()
    if not chat_id:
        raise ValueError("Пустой chat_id")
    with pool.connection() as conn:
        row = conn.execute(
            """
            INSERT INTO telegram_recipients (chat_id, name, username, enabled)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (chat_id) DO UPDATE SET
                name = CASE WHEN EXCLUDED.name <> '' THEN EXCLUDED.name ELSE telegram_recipients.name END,
                username = CASE WHEN EXCLUDED.username <> '' THEN EXCLUDED.username ELSE telegram_recipients.username END,
                enabled = TRUE
            RETURNING id, chat_id, name, username, enabled, created_at
            """,
            (chat_id, name.strip(), username.strip().lstrip("@")),
        ).fetchone()
    return {
        "id": row[0],
        "chat_id": row[1],
        "name": row[2],
        "username": row[3],
        "enabled": row[4],
        "created_at": row[5].isoformat(),
    }


def set_recipient_enabled(recipient_id: int, enabled: bool) -> None:
    with pool.connection() as conn:
        row = conn.execute(
            "UPDATE telegram_recipients SET enabled = %s WHERE id = %s RETURNING id",
            (enabled, recipient_id),
        ).fetchone()
    if not row:
        raise KeyError(recipient_id)


def delete_recipient(recipient_id: int) -> None:
    with pool.connection() as conn:
        row = conn.execute(
            "DELETE FROM telegram_recipients WHERE id = %s RETURNING id",
            (recipient_id,),
        ).fetchone()
    if not row:
        raise KeyError(recipient_id)


def pending_chats() -> list[dict]:
    """Люди, которые написали боту /start, но ещё не в списке получателей."""
    known = {r["chat_id"] for r in list_recipients()}
    data = telegram_api("getUpdates", {"timeout": 0, "limit": 50})
    if not data.get("ok"):
        return []
    pending: dict[str, dict] = {}
    join_code = settings.telegram_join_code.strip()
    for upd in data.get("result") or []:
        msg = upd.get("message") or upd.get("channel_post") or {}
        chat = msg.get("chat") or {}
        chat_id = str(chat.get("id") or "")
        if not chat_id or chat_id in known:
            continue
        text = (msg.get("text") or "").strip()
        first = chat.get("first_name") or chat.get("title") or ""
        last = chat.get("last_name") or ""
        name = f"{first} {last}".strip() or "Без имени"
        username = chat.get("username") or ""
        if join_code and text.lower().startswith("/join"):
            parts = text.split(maxsplit=1)
            if len(parts) == 2 and parts[1].strip() == join_code:
                rec = upsert_recipient(chat_id, name, username)
                send_welcome(chat_id)
                known.add(chat_id)
                continue
        pending[chat_id] = {
            "chat_id": chat_id,
            "name": name,
            "username": username,
            "type": chat.get("type") or "private",
            "text": text[:80],
        }
    return list(pending.values())


def send_welcome(chat_id: str) -> None:
    telegram_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Готово. Сюда будут приходить новые заявки с сайта Грэйдстрой.",
        },
    )


def _lead_text(
    lead_id: int,
    name: str,
    phone: str,
    has_drawing: bool,
    comment: str,
    file_name: str,
    source: str,
) -> str:
    shown = pretty_phone(phone) or phone
    lines = [
        f"<b>Новая заявка #{lead_id}</b>",
        "",
        f"📞 <code>{_esc(shown)}</code>",
    ]
    if name:
        lines.append(f"👤 {_esc(name)}")
    lines.append(f"📐 Чертёж: {'есть' if has_drawing else 'нет'}")
    if file_name:
        lines.append(f"📎 {_esc(file_name)}")
    if source:
        lines.append(f"🌐 {_esc(_page_label(source))}")
    if comment:
        text = comment if len(comment) <= 1200 else comment[:1200] + "…"
        lines.extend(["", _esc(text)])
    return "\n".join(lines)


def notify_new_lead(
    lead_id: int,
    name: str,
    phone: str,
    has_drawing: bool,
    comment: str,
    file_name: str,
    source: str,
    file_path: str = "",
) -> None:
    if not telegram_configured():
        return
    pending_chats()
    chats = enabled_chat_ids()
    if not chats:
        log.info("Заявка #%s: бот есть, но получатели Telegram не заданы", lead_id)
        return

    text = _lead_text(lead_id, name, phone, has_drawing, comment, file_name, source)
    contact_phone = international_phone(phone)
    disk = UPLOAD_DIR / Path(file_path).name if file_path else None
    send_file = bool(disk and disk.is_file() and disk.stat().st_size <= TG_FILE_LIMIT)

    for chat_id in chats:
        msg = telegram_api(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
        )
        mid = ((msg.get("result") or {}) if msg.get("ok") else {}).get("message_id")
        reply = {"reply_to_message_id": mid} if mid else {}

        if contact_phone:
            telegram_api(
                "sendContact",
                {
                    "chat_id": chat_id,
                    "phone_number": contact_phone,
                    "first_name": (name or "Заявка").strip()[:64] or "Заявка",
                    "last_name": f"заявка {lead_id}",
                    **reply,
                },
            )
        if send_file and disk:
            telegram_api(
                "sendDocument",
                {
                    "chat_id": chat_id,
                    "caption": file_name or disk.name,
                    **reply,
                },
                file=disk,
            )


def send_test() -> dict:
    chats = enabled_chat_ids()
    if not telegram_configured():
        return {"ok": False, "error": "Токен бота не задан"}
    if not chats:
        return {"ok": False, "error": "Нет получателей"}
    ok = 0
    for chat_id in chats:
        res = telegram_api(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Тест Грэйдстрой: уведомления о заявках доходят.",
            },
        )
        if res.get("ok"):
            ok += 1
    return {"ok": ok > 0, "sent": ok, "total": len(chats)}
