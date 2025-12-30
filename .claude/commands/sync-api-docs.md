# Sync API Documentation

Automatically sync API documentation with the actual OpenAPI schema.

## Instructions

1. **Start the server** (if not running):

   ```bash
   cd week4
   make run &
   sleep 3
   ```

2. **Fetch current OpenAPI schema**:

   ```bash
   curl -s http://localhost:8000/openapi.json > /tmp/openapi_current.json
   ```

3. **Analyze the schema**:
   - Parse the OpenAPI JSON
   - Extract all endpoints, methods, parameters, and response schemas
   - Group by tags/routers

4. **Check if API.md exists**:
   - If `week4/docs/API.md` doesn't exist, create it
   - If it exists, read its current content

5. **Generate/Update API.md**:
   - Create a well-formatted markdown document with:
     - Table of contents
     - Endpoints organized by router/tag
     - For each endpoint:
       - HTTP method and path
       - Description
       - Request parameters (path, query, body)
       - Request body schema (if applicable)
       - Response schema
       - Example request/response
   - Use tables and code blocks for clarity

6. **Detect changes**:
   - If updating existing API.md:
     - Compare old vs new content
     - List added endpoints
     - List removed endpoints
     - List modified endpoints
   - Provide a diff-like summary

7. **Save the updated documentation**:
   - Write the new API.md
   - Show a summary of changes

8. **Verify completeness**:
   - Check that all routes from OpenAPI are documented
   - Flag any undocumented endpoints
   - Suggest adding descriptions where missing

## Expected Output

- "✅ API.md updated successfully"
- Summary of changes:
  - Added: X endpoints
  - Removed: Y endpoints
  - Modified: Z endpoints
- List of specific changes
- TODOs for missing descriptions

## Safety Notes

- Only reads from server and writes to docs/API.md
- Safe to run anytime after code changes
- Non-destructive: can regenerate anytime

## Rollback

- Restore with: `git checkout -- week4/docs/API.md`
