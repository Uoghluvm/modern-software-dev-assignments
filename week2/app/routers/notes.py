"""
TODO 3 Refactored: Notes Router with proper API schemas and error handling.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..schemas import CreateNoteRequest, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(request: CreateNoteRequest) -> NoteResponse:
    """
    Create a new note.
    
    Args:
        request: CreateNoteRequest with note content
        
    Returns:
        NoteResponse with created note details
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        note_id = db.insert_note(request.content)
        note = db.get_note(note_id)
        
        if note is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created note"
            )
            
        return NoteResponse(
            id=note["id"],
            content=note["content"],
            created_at=note["created_at"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create note: {str(e)}"
        )


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """
    Get a single note by ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        NoteResponse with note details
        
    Raises:
        HTTPException: If note not found
    """
    try:
        row = db.get_note(note_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with ID {note_id} not found"
            )
        return NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve note: {str(e)}"
        )


# TODO 4: Endpoint to retrieve all notes
@router.get("", response_model=List[NoteResponse])
def list_all_notes() -> List[NoteResponse]:
    """
    Retrieve all notes.
    
    Returns:
        List of NoteResponse objects
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        rows = db.list_notes()
        return [
            NoteResponse(
                id=row["id"],
                content=row["content"],
                created_at=row["created_at"]
            )
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notes: {str(e)}"
        )

