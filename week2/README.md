# Action Item Extractor

A FastAPI-based web application that intelligently extracts actionable items from free-form notes using both rule-based heuristics and AI-powered LLM analysis.

## 🌟 Features

- **Dual Extraction Methods**:
  - **Rule-based**: Fast heuristic extraction using pattern matching for bullets, checkboxes, and keywords
  - **LLM-powered**: AI-driven extraction using Ollama that understands context and narrative text

- **Note Management**:
  - Save notes to SQLite database
  - View all saved notes with timestamps
  - Link action items to their source notes

- **Interactive UI**:
  - Clean, modern web interface
  - Real-time action item extraction
  - Checkbox tracking for completed items
  - Visual badges to distinguish extraction methods

## 🏗️ Architecture

```
week2/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database layer (SQLite)
│   ├── schemas.py           # Pydantic models for API contracts
│   ├── routers/
│   │   ├── action_items.py  # Action items endpoints
│   │   └── notes.py         # Notes endpoints
│   └── services/
│       └── extract.py       # Extraction logic (rule-based & LLM)
├── frontend/
│   └── index.html          # Single-page web interface
├── tests/
│   └── test_extract.py     # Unit tests for extraction functions
└── data/
    └── app.db              # SQLite database (created at runtime)
```

## 📋 Prerequisites

- Python 3.12+
- Conda (for environment management)
- Poetry (for dependency management)
- Ollama (for LLM-based extraction)

## 🚀 Setup and Installation

### 1. Clone the Repository

```bash
cd modern-software-dev-assignments
```

### 2. Set Up Conda Environment

```bash
conda activate cs146s
```

### 3. Install Dependencies

Dependencies are managed via Poetry and should already be installed. If not:

```bash
poetry install
```

### 4. Set Up Ollama

Install Ollama and pull a model (e.g., llama3.1:8b):

```bash
# Install Ollama (visit https://ollama.com)
ollama pull llama3.1:8b
```

## 🎮 Usage

### Starting the Server

From the project root directory:

```bash
poetry run uvicorn week2.app.main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

### Using the Web Interface

1. **Open your browser** and navigate to `http://127.0.0.1:8000/`

2. **Enter notes** in the text area. Try any format:
   ```
   - [ ] Buy groceries
   TODO: Call the dentist
   We should schedule a team meeting
   * Fix the login bug
   ```

3. **Choose an extraction method**:
   - **Extract (Rule-based)**: Fast, pattern-based extraction
   - **Extract (LLM)**: AI-powered, context-aware extraction

4. **Optional**: Check "Save as note" to persist your notes

5. **View saved notes**: Click "List Notes" to see all previously saved notes

## 📡 API Endpoints

### Action Items

#### `POST /action-items/extract`
Extract action items using rule-based heuristics.

**Request Body:**
```json
{
  "text": "Your notes here",
  "save_note": true
}
```

**Response:**
```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Buy groceries",
      "note_id": 1,
      "done": false
    }
  ]
}
```

#### `POST /action-items/extract-llm`
Extract action items using LLM (Ollama).

Same request/response format as `/extract` endpoint.

#### `GET /action-items`
List all action items, optionally filtered by `note_id`.

**Query Parameters:**
- `note_id` (optional): Filter by note ID

#### `POST /action-items/{action_item_id}/done`
Mark an action item as done/undone.

**Request Body:**
```json
{
  "done": true
}
```

### Notes

#### `POST /notes`
Create a new note.

**Request Body:**
```json
{
  "content": "Your note content"
}
```

#### `GET /notes`
Retrieve all notes.

#### `GET /notes/{note_id}`
Get a specific note by ID.

## 🧪 Running Tests

### Run All Tests

```bash
conda run -n cs146s poetry run pytest week2/tests/ -v
```

### Run Specific Test File

```bash
conda run -n cs146s poetry run pytest week2/tests/test_extract.py -v
```

### Test Coverage

The test suite includes:
- ✅ Rule-based extraction tests
- ✅ LLM extraction tests (7 test cases covering various scenarios)
- ✅ Empty input handling
- ✅ Deduplication logic
- ✅ Mixed format parsing

## 🛠️ Development

### Code Structure

- **Pydantic Schemas** (`schemas.py`): Type-safe API contracts
- **Database Layer** (`db.py`): SQLite operations with connection management
- **Service Layer** (`services/extract.py`): Business logic for extraction
- **Routers** (`routers/`): FastAPI endpoints with proper error handling

### Key Design Decisions

1. **Pydantic Models**: Ensures type safety and automatic validation
2. **Structured LLM Output**: Uses Pydantic schema with Ollama for consistent JSON responses
3. **Fallback Strategy**: LLM extraction falls back to rule-based on errors
4. **Database Transactions**: Proper connection management with context managers
5. **Error Handling**: Comprehensive try-catch blocks with meaningful error messages

## 🔄 TODO Completion Status

- ✅ **TODO 1**: Implemented `extract_action_items_llm()` with Ollama structured outputs
- ✅ **TODO 2**: Added comprehensive unit tests (8 tests, all passing)
- ✅ **TODO 3**: Refactored code with Pydantic schemas, error handling, and proper API contracts
- ✅ **TODO 4**: Added LLM extraction endpoint and List Notes functionality
- ✅ **TODO 5**: Generated comprehensive README documentation

## 🎯 Example Use Cases

### For Developers
```
Meeting notes:
- Need to refactor the authentication module
TODO: Update API documentation
* Fix the memory leak in the caching layer
Should add error handling to the upload endpoint
```

### For Project Managers
```
Sprint planning:
- [ ] Review user stories
- Schedule retrospective meeting
Next: Update project timeline
Action: Send status report to stakeholders
```

### For Personal Tasks
```
Weekend todo:
- Buy groceries
- Call mom
Need to schedule dentist appointment
Should finish reading that book
```

##  Technologies Used

- **Backend**: FastAPI, Python 3.12
- **Database**: SQLite3
- **AI/ML**: Ollama (llama3.1:8b)
- **Validation**: Pydantic v2
- **Testing**: pytest
- **Frontend**: Vanilla HTML/CSS/JavaScript

## 📝 License

This project is part of the CS146 Modern Software Development course assignments.

## 🤝 Contributing

This is a course assignment. For issues or suggestions, please contact the course instructors.

---

**Built with ❤️ for CS146 Modern Software Development**
