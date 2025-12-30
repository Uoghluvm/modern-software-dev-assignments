# Add New API Endpoint

Automate the creation of a new REST API endpoint with tests and documentation.

## Arguments

- `$RESOURCE_NAME`: The resource name (e.g., "tasks", "users")
- `$ENDPOINT_TYPE`: Type of endpoint - "crud" or "custom"
- `$METHOD`: HTTP method (GET, POST, PUT, DELETE) if custom

## Instructions

1. **Gather information**:
   - Ask the user for resource name if not provided
   - Ask for endpoint type (CRUD with all operations or custom single endpoint)
   - For custom endpoints, ask for HTTP method and specific functionality

2. **Create or update the router**:
   - Check if `backend/app/routers/{resource_name}.py` exists
   - If CRUD: Create complete CRUD operations (GET all, GET by id, POST, PUT, DELETE)
   - If custom: Create the specific endpoint requested
   - Use proper FastAPI decorators, dependency injection, and error handling
   - Follow the pattern from existing routers (notes.py, action_items.py)

3. **Update schemas**:
   - Add/update Pydantic models in `backend/app/schemas.py`
   - Include Create, Update, and Response schemas as needed
   - Add proper validation (Field validators, min/max lengths)

4. **Update models** (if new resource):
   - Add SQLAlchemy model in `backend/app/models.py`
   - Include proper relationships and constraints
   - Add created_at/updated_at timestamps

5. **Register the router**:
   - Import the new router in `backend/app/main.py`
   - Add `app.include_router()` call

6. **Create tests**:
   - Create `backend/tests/test_{resource_name}.py`
   - Write tests for all endpoints created
   - Include happy path and error cases
   - Test validation rules

7. **Update documentation**:
   - Add endpoint descriptions to `docs/TASKS.md` if it's a new feature
   - Note the changes made

8. **Verify everything works**:
   - Run `make format` to format the code
   - Run `make lint` to check for issues
   - Run `make test` to ensure tests pass
   - Report any failures and suggest fixes

## Expected Output

- Confirmation of files created/modified
- Test results showing all tests pass
- Next steps (e.g., "Try the endpoint at <http://localhost:8000/docs>")

## Rollback

If something goes wrong:

- New files can be deleted
- Modified files: restore from git with `git checkout -- <file>`

## Safety Notes

- Always run tests after creating new endpoints
- Follow existing code patterns for consistency
- Auto-format with black/ruff before finalizing
