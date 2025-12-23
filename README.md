# DMS‑Showcase

Demo for DMS product with mock‑up data — компактная демоверсия fullstack приложения (Python backend + TypeScript frontend) для демонстрации в резюме и быстрого просмотра функционала.

## Архитектура (кратко)

Ниже — простая ASCII‑диаграмма, чтобы рекрутер/разработчик быстро понял основные компоненты приложения.

Frontend (TypeScript)
  [Browser / UI]
        |
        v
  [Frontend (React/TS)]
        |
        v
  [API (REST / GraphQL)]
        |
        v
  [Backend (Python)]
   /      |       \
  v       v        v
[DB]   [File storage]  [Auth / Mock data]
 (Postgres or mock)    (local / S3 mock)

Дополнительно:
- Docker / Makefile — контейнеризация + локальный запуск
- CI (optional) — запуск тестов / линтинга

---

## Графическая диаграмма (PNG)

---

## Примечание

Я оставил в репозитории `architecture.mmd` — исходную mermaid‑диаграмму — на случай, если вы захотите её править или генерировать другие форматы. Если хотите, уберу её или добавлю более детальную диаграмму по вашему запросу.
