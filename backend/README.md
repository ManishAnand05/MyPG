# MyPG Backend

FastAPI + SQLAlchemy backend for MyPG hostel/PG management system with PostgreSQL (Supabase).

## Setup

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Configure environment**:

Create `.env` file in `backend/app/` directory:

```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3. **Run the server**:

```bash
cd backend
uvicorn app.main:app --reload
```

Server runs at http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

- **Models** (`app/models/`): SQLAlchemy ORM with User → PG → Room → Bed → Tenant relationships
- **Schemas** (`app/schemas/`): Pydantic models for request/response validation
- **Services** (`app/services/`): Business logic layer
- **Routers** (`app/routers/`): FastAPI endpoints
- **Core** (`app/core/`): Database, auth, and security utilities

## Authentication

- JWT tokens in httpOnly cookies (`access_token`)
- Role-based access: `ADMIN` (can create PGs) and `TENANT`
- Protected endpoints use `get_current_user` dependency

## Key Endpoints

### Auth
- `POST /auth/signup` - Create new user
- `POST /auth/login` - Login (sets cookie)
- `POST /auth/logout` - Clear auth cookie
- `GET /auth/me` - Get current user

### PGs
- `GET /pg/get` - List all PGs
- `POST /pg/create` - Create PG (admin only)

### Rooms
- `GET /rooms/{pg_id}` - List rooms for a PG
- `POST /rooms/create` - Create room

### Beds
- `GET /beds/{room_id}` - List beds in a room
- `POST /beds/create` - Create bed

### Tenants
- `GET /tenants/` - List all tenants
- `POST /tenants/create` - Create tenant profile

## Database

Uses PostgreSQL via Supabase. Tables are created manually or via commented `create_all` in `main.py`. Alembic migrations not yet implemented.

## Dependencies

See `requirements.txt`:
- FastAPI 0.128.0
- SQLAlchemy 2.0.46
- Pydantic 2.12.5
- python-jose 3.5.0
- passlib 1.7.4
- psycopg2-binary 2.9.11
- uvicorn 0.40.0