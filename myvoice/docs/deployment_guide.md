# MyVoice Deployment Guide

> **최종 업데이트**: 2026-03-06

This guide describes how to deploy the MyVoice application to a production server (Ubuntu/Debian) using Docker Compose.

## Prerequisites

- A Linux server (Ubuntu 22.04 LTS recommended)
- `docker` and `docker compose` installed
- Git installed
- Node.js 18+ (for frontend build)
- Domain name pointed to your server IP (optional, but recommended for SSL)

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/myvoice.git
cd myvoice
```

## Step 2: Configure Environment Variables

Create a `.env.prod` file based on `.env.example`.

```bash
cp .env.example .env.prod
nano .env.prod
```

**Critical Variables to Set:**
- `APP_ENV=production`
- `DATABASE_URL`: Ensure credentials match `docker-compose.prod.yml` or your external DB.
- `JWT_SECRET_KEY`: Generate a secure random string (e.g., `openssl rand -hex 32`).
- `OPENAI_API_KEY`: Your real OpenAI API key.
- `DB_PASSWORD`: Set a strong password for PostgreSQL.

## Step 3: Build Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

The build output will be in `frontend/dist/`. This is served by Nginx in the Docker setup.

## Step 4: Run with Docker Compose

Build and start the containers in detached mode.

```bash
# Provide the DB_PASSWORD environment variable inline or export it
DB_PASSWORD=your_secure_db_password docker compose -f docker-compose.prod.yml up -d --build
```

## Step 5: Run Migrations

Initialize the database schema.

```bash
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## Step 6: Seed Data (First Deploy Only)

```bash
docker compose -f docker-compose.prod.yml exec backend python -m app.seed
```

## Step 7: Verify Deployment

Check container status:

```bash
docker compose -f docker-compose.prod.yml ps
```

Check logs:

```bash
docker compose -f docker-compose.prod.yml logs -f backend
```

Access the application at `http://<your-server-ip>`.

## Local Development

```bash
# Backend
cd myvoice
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd myvoice/frontend
npm run dev   # Starts on port 5173, proxies /v1/* to localhost:8000
```

## Troubleshooting

- **502 Bad Gateway**: Check backend logs (`docker compose logs backend`). Nginx might be unable to reach the backend service.
- **Database Connection Error**: Verify `DATABASE_URL` matches the service name `db` in `docker-compose.prod.yml`.
- **Permission Denied (Docker)**: Ensure your user is in the `docker` group (`sudo usermod -aG docker $USER`).
- **Frontend Build Fails**: Ensure Node.js 18+ is installed. Run `npm install` before `npm run build`.
- **Missing Seed Data**: Run `python -m app.seed` to populate vocabulary categories, shop items, and curriculum data.
