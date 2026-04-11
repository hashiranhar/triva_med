# RefugeesMH

A mental health intake and triage platform for refugee patients.

## Structure

```
backend/        FastAPI + SQLite backend
  main.py       API endpoints
  models.py     SQLAlchemy ORM models
  schemas.py    Pydantic request/response models
  database.py   DB engine + session

dashboard/
  dashboard.py  Streamlit clinician dashboard
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

## Running

```bash
# Terminal 1 — backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — dashboard
streamlit run dashboard/dashboard.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET    | /api/v1/health | Health check |
| POST   | /api/v1/session/start | Create a session |
| POST   | /api/v1/submission | Submit patient intake form |
| GET    | /api/v1/queue | Get all unseen patients |
| PATCH  | /api/v1/submission/{id}/seen | Mark patient as seen |
| GET    | /api/v1/submission/{id} | Get single submission |