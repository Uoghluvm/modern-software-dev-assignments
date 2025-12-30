# Week 4 Write-up

## SUBMISSION DETAILS

Name: **[Your Name]**
SUNet ID: **[Your ID]**
Citations: **Claude Code Documentation**

This assignment took me about **2** hours to do.

## YOUR RESPONSES

### Automation #1

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> I was inspired by the need for consistent and rapid API development. Managing boilerplate for new endpoints (models, schemas, routers, tests) is tedious and prone to error. The [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) suggest automating repeated workflows to maintain focus on high-level logic.

b. Design of each automation, including goals, inputs/outputs, steps
> **Command:** `/add-endpoint`
> **Goal:** Automate the creation of a new REST API endpoint with all necessary files (Router, Model, Schema, Test).
> **Inputs:** Resource name (e.g., "tags"), type (CRUD/Custom).
> **Outputs:** Created/Updates files in `backend/app/` and `backend/tests/`.
> **Steps:**
>
> 1. Collect resource details from user.
> 2. Create Pydantic schemas in `schemas.py`.
> 3. Add SQLAlchemy model to `models.py`.
> 4. Create router file in `routers/` with standard CRUD operations.
> 5. Create specific tests in `tests/`.
> 6. Register router in `main.py`.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Command:** `/add-endpoint` (trigger via Slash Command)
> **Expected Output:** A series of file creations and a confirmation that the endpoint is ready to test.
> **Safety:** Runs tests immediately after generation. Rollback via `git checkout`.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Manually creating 4-5 files, copy-pasting code, manually renaming variables, often forgetting to register the router or add a test.
> **After:** Single command prompts for the name, and within seconds, a fully functioning, tested endpoint implementation exists.

e. How you used the automation to enhance the starter application
> I used this automation to generate the **Tags** feature. I ran `/add-endpoint` with resource name "tags", and it scaffolded the schemas, model, and router. I then refined the logic to add color support and uniqueness constraints.

### Automation #2

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Keeping documentation in sync with code is a classic problem. Inspired by "Docs as Code" principles, I wanted a way to ensure `docs/API.md` always reflects the actual running server's OpenAPI schema.

b. Design of each automation, including goals, inputs/outputs, steps
> **Command:** `/sync-api-docs`
> **Goal:** Sync `docs/API.md` with the live OpenAPI schema from the running FastAPI app.
> **Inputs:** None (reads from localhost:8000).
> **Outputs:** Updated `docs/API.md` file.
> **Steps:**
>
> 1. Fetch JSON from `http://localhost:8000/openapi.json`.
> 2. Parse endpoints and schema definitions.
> 3. Format into a readable Markdown table/list.
> 4. Overwrite `docs/API.md`.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Command:** `/sync-api-docs`
> **Prerequisites:** Server must be running (`make run`).
> **Expected Output:** "✅ API.md updated successfully".
> **Safety:** Only modifies documentation.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Manually editing markdown tables whenever a parameter changed or an endpoint was added.
> **After:** One command ensures documentation is 100% accurate to the code.

e. How you used the automation to enhance the starter application
> After adding the **Tags** endpoints, I ran this command to automatically generate the documentation for `GET /tags`, `POST /tags`, etc., ensuring the new feature was documented without manual effort.

### *(Optional) Automation #3*

*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Making it easier to run tests and see coverage without remembering flags.

b. Design of each automation, including goals, inputs/outputs, steps
> **Command:** `/test-coverage`
> **Goal:** Run tests with coverage reporting.
> **Steps:** Runs pytest with coverage flags and summarizes output.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Command:** `/test-coverage`
> **Output:** Pass/Fail status and % coverage.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Typing long pytest commands.
> **After:** Simple slash command.

e. How you used the automation to enhance the starter application
> Used to verify the **Tags** feature had adequate test coverage.
