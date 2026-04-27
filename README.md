# SyncBase

A modern file synchronization and sharing platform built with FastAPI.

## 🎯 Overview

SyncBase is a self-hosted cloud storage solution designed to provide secure file storage, synchronization, version control, and collaborative sharing capabilities.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework for building APIs
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Reliable relational database with SQLAlchemy ORM
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation and serialization
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database schema versioning
- **Settings**: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Configuration management
- **Python**: 3.13+

## 📋 Prerequisites

### System Requirements

- **Python**: 3.13 or higher
- **PostgreSQL**: 12 or higher
- **pip**: Python package manager (comes with Python)
- **Virtual Environment**: venv (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/syncbase.git
   cd syncbase
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   On Windows:

   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

   On Unix/MacOS:

   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -e .
   ```

   This installs all packages defined in `pyproject.toml`:
   - FastAPI with standard dependencies
   - PostgreSQL adapter (psycopg2-binary)
   - Pydantic Settings
   - SQLAlchemy

## 📦 Dependencies

Core dependencies (from `pyproject.toml`):

```toml
dependencies = [
    "fastapi[standard]>=0.136.0",      # Web framework with Uvicorn, Starlette, etc.
    "psycopg2-binary>=2.9.12",         # PostgreSQL adapter
    "pydantic-settings>=2.14.0",       # Configuration management
    "sqlalchemy>=2.0.49",              # ORM and database toolkit
]
```

## 🗂️ Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── core/
│   ├── config.py          # Configuration and settings
│   └── database.py        # Database connection and session
├── models/                # SQLAlchemy ORM models
├── schemas/               # Pydantic request/response schemas
├── routers/               # API routes
├── services/              # Business logic
├── storage/               # Storage backends
├── middleware/            # Custom middleware
└── utils/                 # Utility functions
```

## 🚀 Getting Started

After installation, you can verify your setup:

```bash
# Verify Python version
python --version

# Verify dependencies are installed
pip list

# Start the FastAPI development server
uvicorn app.main:app --reload
```

The application will run at `http://localhost:8000`

---

**Project**: SyncBase - File Synchronization Platform
