# API Documentation

## Table of Contents

- [Notes](#notes)
- [Action Items](#action-items)
- [Tags](#tags)

---

## Notes

### GET /notes/

List all notes.

- **Response**: `List[NoteRead]`

### POST /notes/

Create a new note.

- **Body**: `NoteCreate`

  ```json
  {
    "title": "string",
    "content": "string"
  }
  ```

- **Response**: `NoteRead`

### GET /notes/search/

Search notes by query string.

- **Query Parameters**:
  - `q`: string (optional)
- **Response**: `List[NoteRead]`

### GET /notes/{note_id}

Get a specific note by ID.

- **Path Parameters**:
  - `note_id`: integer
- **Response**: `NoteRead`

---

## Action Items

### GET /action-items/

List all action items.

- **Response**: `List[ActionItemRead]`

### POST /action-items/

Create a new action item.

- **Body**: `ActionItemCreate`

  ```json
  {
    "description": "string"
  }
  ```

- **Response**: `ActionItemRead`

### PUT /action-items/{item_id}/complete

Mark an action item as completed.

- **Path Parameters**:
  - `item_id`: integer
- **Response**: `ActionItemRead`

---

## Tags

### GET /tags/

List all tags.

- **Response**: `List[TagRead]`

### POST /tags/

Create a new tag.

- **Body**: `TagCreate`

  ```json
  {
    "name": "string",
    "color": "string" 
  }
  ```

- **Response**: `TagRead`

### GET /tags/{tag_id}

Get a specific tag by ID.

- **Path Parameters**:
  - `tag_id`: integer
- **Response**: `TagRead`

### PUT /tags/{tag_id}

Update a tag.

- **Path Parameters**:
  - `tag_id`: integer
- **Body**: `TagUpdate`

  ```json
  {
    "name": "string", 
    "color": "string"
  }
  ```

- **Response**: `TagRead`

### DELETE /tags/{tag_id}

Delete a tag.

- **Path Parameters**:
  - `tag_id`: integer
- **Response**: 204 No Content
