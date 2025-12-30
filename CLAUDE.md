# Week 4 - Developer's Command Center

This repository contains a modern software development assignment focusing on autonomous coding agent workflows.

## Project Structure

```
week4/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py       # FastAPI app entry point
│   │   ├── db.py         # Database configuration
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── routers/      # API route handlers
│   │   │   ├── notes.py
│   │   │   └── action_items.py
│   │   └── services/     # Business logic
│   │       └── extract.py
│   └── tests/         # Pytest test suite
├── frontend/          # Static HTML/JS/CSS UI
├── data/              # SQLite database + seed data
├── docs/              # Documentation and task lists
│   └── TASKS.md       # Development tasks
└── Makefile           # Common commands
```

## Quick Commands

- **Run app**: `cd week4 && make run` (or `PYTHONPATH=. uvicorn backend.app.main:app --reload`)
- **Run tests**: `cd week4 && make test`
- **Format code**: `cd week4 && make format`
- **Lint code**: `cd week4 && make lint`
- **View API docs**: Start app, then visit `http://localhost:8000/docs`

## Development Workflow Best Practices

### When Adding a New Feature

1. **Test-Driven Development**:
   - Write a failing test first in `backend/tests/test_*.py`
   - Implement the feature
   - Run tests to verify: `make test`

2. **Code Quality**:
   - Always run `make format` before committing
   - Ensure `make lint` passes without errors
   - If pre-commit is installed, it will run automatically

3. **API Endpoint Workflow**:
   - Add route in `backend/app/routers/`
   - Define schemas in `schemas.py`
   - Add/update models in `models.py` if needed
   - Register router in `main.py`
   - Write comprehensive tests
   - Update documentation in `docs/`

### Safety Guidelines

**Safe to auto-run**:

- `make test` - runs pytest
- `make lint` - runs ruff check (read-only)
- `make format` - runs black + ruff fix (formats code)
- Reading files, viewing API docs

**Requires user approval**:

- `make run` - starts server (long-running process)
- Database migrations or seed data changes
- Deleting files or endpoints
- Installing new dependencies

### Code Style Expectations

- **Formatting**: Use `black` (line length 88)
- **Linting**: Follow `ruff` rules
- **Type hints**: Use Python type annotations where possible
- **Docstrings**: Add docstrings to public functions/classes
- **Error handling**: Return appropriate HTTP status codes (400, 404, 500)
- **Testing**: Aim for high coverage (80%+), test both happy and error paths

## Common Patterns

### Adding a Route

```python
@router.post("/{resource}", response_model=schemas.ResourceResponse)
def create_resource(
    resource: schemas.ResourceCreate,
    db: Session = Depends(get_db)
):
    # Implementation
    pass
```

### Adding a Test

```python
def test_create_resource(client):
    response = client.post("/{resource}", json={...})
    assert response.status_code == 200
    assert response.json()["field"] == "expected"
```

### Schema Pattern

```python
class ResourceBase(BaseModel):
    field: str

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Custom Slash Commands Available

- `/test-coverage` - Run tests with coverage analysis
- `/add-endpoint` - Scaffold a new API endpoint with tests
- `/sync-api-docs` - Sync API documentation with OpenAPI schema

## When Working on Tasks

Reference `docs/TASKS.md` for planned features. When completing a task:

1. Understand the requirement fully
2. Check existing code patterns
3. Implement with tests
4. Verify with `make test && make lint`
5. Update documentation as needed

## Database

- **Type**: SQLite
- **Location**: `data/app.db`
- **ORM**: SQLAlchemy
- **Migrations**: Currently using `Base.metadata.create_all()` (no Alembic yet)
- **Seed**: Run `make seed` or happens automatically on startup

## Debugging Tips

- Check FastAPI auto-docs: `http://localhost:8000/docs`
- View OpenAPI schema: `http://localhost:8000/openapi.json`
- Run single test: `PYTHONPATH=. pytest backend/tests/test_file.py::test_name -v`
- Check database: `sqlite3 data/app.db` then `.tables` or `.schema`

## Current Features

- **Notes**: CRUD operations for notes (list, create, get by ID)
- **Action Items**: Create and list action items
- **Extraction**: Parse action items from note content
- **Frontend**: Basic UI for interacting with notes and action items

## Planned Improvements (see docs/TASKS.md)

- Search endpoint for notes
- Complete action items flow
- Enhanced extraction (tags, priorities)
- Full CRUD for notes (edit, delete)
- Request validation and error handling
