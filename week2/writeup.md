# Week 2 Write-up

Tip: To preview this markdown file

- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **[Student Name]** \
SUNet ID: **[SUNetID]** \
Citations: Ollama documentation (<https://ollama.com/blog/structured-outputs>), FastAPI documentation, Pydantic documentation

This assignment took me about **3-4** hours to do.

## YOUR RESPONSES

For each exercise, please include what prompts used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature

Prompt:

```
Implement an LLM-powered alternative extraction function called extract_action_items_llm() 
that uses Ollama to extract action items from text. Use Pydantic models for structured 
outputs to ensure the LLM returns a JSON array of strings. The function should:
1. Use the llama3.1:8b model
2. Accept text as input and return a List[str] of action items
3. Include a system prompt that instructs the LLM to extract action items
4. Use Ollama's structured output capability with Pydantic schema
5. Deduplicate results
6. Fall back to rule-based extraction on errors
```

Generated Code Snippets:

```
File: week2/app/services/extract.py
- Lines 93-176: Added ActionItemsResponse Pydantic model (lines 93-96)
- Lines 99-176: Implemented extract_action_items_llm() function with:
  - System prompt for LLM guidance (lines 111-122)
  - Ollama chat API integration (lines 127-137)
  - Structured output using Pydantic schema (line 137)
  - JSON parsing and deduplication logic (lines 140-156)
  - Error handling with fallback (lines 158-161)
```

### Exercise 2: Add Unit Tests

Prompt:

```
Write comprehensive unit tests for the extract_action_items_llm() function in 
week2/tests/test_extract.py. Tests should cover:
1. Bullet-point lists with checkboxes
2. Keyword-prefixed items (TODO:, Action:, Next:)
3. Empty input
4. Mixed format notes
5. Narrative text without explicit markers
6. Deduplication of identical items
7. Purely narrative text with no action items

Use flexible assertions since LLM responses may vary.
```

Generated Code Snippets:

```
File: week2/tests/test_extract.py
- Lines 5: Updated imports to include extract_action_items_llm
- Lines 23-129: Added TestExtractActionItemsLLM class with 7 test methods:
  - test_llm_extract_bullet_list() (lines 26-36)
  - test_llm_extract_keyword_prefixed() (lines 38-49)
  - test_llm_extract_empty_input() (lines 51-55)
  - test_llm_extract_mixed_format() (lines 57-70)
  - test_llm_extract_narrative_text() (lines 72-88)
  - test_llm_extract_no_duplicates() (lines 90-102)
  - test_llm_extract_only_narrative() (lines 104-115)

All 8 tests passed (including the original rule-based test).
```

### Exercise 3: Refactor Existing Code for Clarity

Prompt:

```
Refactor the backend code to improve clarity and maintainability by:
1. Creating Pydantic schemas for all API request/response models
2. Replacing Dict[str, Any] with proper typed models
3. Adding comprehensive error handling with try-catch blocks
4. Improving function documentation
5. Using proper HTTP status codes
6. Adding response_model to all endpoints
```

Generated/Modified Code Snippets:

```
File: week2/app/schemas.py (NEW FILE)
- Lines 1-66: Created Pydantic models for API contracts:
  - ExtractRequest (lines 15-19)
  - CreateNoteRequest (lines 22-25)
  - MarkDoneRequest (lines 28-31)
  - ActionItemResponse (lines 34-43)
  - ExtractResponse (lines 46-49)
  - NoteResponse (lines 52-57)
  - ErrorResponse (lines 60-63)

File: week2/app/routers/action_items.py
- Lines 1-3: Added module docstring
- Lines 7-8: Updated imports to use schemas and status codes
- Lines 12-17: Imported Pydantic schemas
- Lines 23-61: Refactored extract() endpoint with:
  - Pydantic request/response models
  - Try-catch error handling
  - Proper HTTP status codes
  - Detailed docstrings
- Lines 64-111: Refactored list_all() endpoint
- Lines 114-137: Refactored mark_done() endpoint

File: week2/app/routers/notes.py
- Lines 1-3: Added module docstring
- Lines 7-8: Updated imports
- Lines 11-13: Imported schemas
- Lines 16-53: Refactored create_note() endpoint
- Lines 56-87: Refactored get_single_note() endpoint
- Lines 90-116: Added list_all_notes() endpoint (for TODO 4)
```

### Exercise 4: Use Agentic Mode to Automate a Small Task

Prompt:

```
1. Add a new endpoint /action-items/extract-llm that uses the LLM extraction function.
2. Update the frontend to add an "Extract (LLM)" button that calls this new endpoint.
3. Add a "List Notes" button that fetches and displays all notes from the /notes endpoint.
4. Improve the UI with better styling, loading states, and organized layout.
```

Generated Code Snippets:

```
File: week2/app/routers/action_items.py
- Line 11: Updated import to include extract_action_items_llm
- Lines 64-111: Added extract_llm() endpoint at /action-items/extract-llm
  - Same structure as extract() but uses extract_action_items_llm()
  - Proper error handling and documentation

File: week2/frontend/index.html
- Lines 7-33: Enhanced CSS styling:
  - Background colors and shadows
  - Button styling with hover effects
  - Note card layouts
  - Badge components
- Lines 37-60: Updated HTML structure:
  - Added section wrapper for better organization
  - Three buttons: Extract (Rule-based), Extract (LLM), List Notes
  - Separate sections for items and notes display
- Lines 186-195: Added button element references
- Lines 197-237: Implemented extractItems() function:
  - Shared extraction logic for both methods
  - Loading states and button disable
  - Error handling with user-friendly messages
  - Badge display (AI Powered vs Rule-based)
- Lines 240-244: Added event listeners for all three buttons
- Lines 247-279: Implemented listNotesBtn click handler:
  - Fetches notes from /notes endpoint
  - Displays notes in card format with timestamps
  - Proper error handling

UI Improvements:
- Modern card-based layout
- Color-coded buttons (blue for rule-based, purple for LLM, green for list notes)
- Badges to distinguish extraction methods
- Loading states for all async operations
- Responsive design with proper spacing
```

### Exercise 5: Generate a README from the Codebase

Prompt:

```
Analyze the current codebase and generate a comprehensive README.md file that includes:
1. Project overview and features
2. Architecture diagram (text-based)
3. Prerequisites and setup instructions
4. Usage guide with examples
5. Complete API documentation for all endpoints
6. Testing instructions
7. Development notes and design decisions
8. TODO completion status
9. Example use cases for different user types
10. Technologies used
```

Generated Code Snippets:

```
File: week2/README.md (NEW FILE)  
- Lines 1-302: Comprehensive README documentation including:
  - Project title and feature overview (lines 1-28)
  - Architecture tree structure (lines 30-50)
  - Prerequisites list (lines 52-57)
  - Setup and installation steps (lines 59-85)
  - Usage guide with examples (lines 87-112)
  - Complete API documentation for all endpoints (lines 114-208)
  - Testing instructions with examples (lines 210-234)
  - Development notes and design decisions (lines 236-266)
  - TODO completion checklist (lines 268-275)
  - Example use cases for developers, PMs, and personal tasks (lines 277-307)
  - Technologies stack (lines 309-318)
  - License and contributing information (lines 320-328)

The README was generated by analyzing:
- All Python files in app/ directory
- Frontend code structure
- Database schema from db.py
- Test files for understanding functionality
- API endpoint definitions
- Pydantic schemas for documentation
```

## SUBMISSION INSTRUCTIONS

1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields.
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope.
