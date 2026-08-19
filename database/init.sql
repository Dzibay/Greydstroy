-- Схема PostgreSQL для сайта Грэйдстрой.
-- Идемпотентно (CREATE IF NOT EXISTS): выполняется при первом старте контейнера postgres
-- (docker-entrypoint-initdb.d) и повторно бэкендом при старте (ensure_schema).

CREATE TABLE IF NOT EXISTS leads (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL DEFAULT '',
    phone TEXT NOT NULL,
    has_drawing BOOLEAN NOT NULL DEFAULT TRUE,
    comment TEXT NOT NULL DEFAULT '',
    file_name TEXT NOT NULL DEFAULT '',
    file_path TEXT NOT NULL DEFAULT '',
    file_size BIGINT NOT NULL DEFAULT 0,
    file_mime TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE leads ADD COLUMN IF NOT EXISTS file_path TEXT NOT NULL DEFAULT '';
ALTER TABLE leads ADD COLUMN IF NOT EXISTS file_size BIGINT NOT NULL DEFAULT 0;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS file_mime TEXT NOT NULL DEFAULT '';

CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads (created_at DESC);
