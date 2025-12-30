"""
TODO 3: Pydantic schemas for API contracts.

This module defines well-structured API request/response models
to ensure type safety and automatic validation.
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# Request Schemas
class ExtractRequest(BaseModel):
    """Request model for action item extraction."""
    text: str = Field(..., min_length=1, description="The text content to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the note to database")


class CreateNoteRequest(BaseModel):
    """Request model for creating a new note."""
    content: str = Field(..., min_length=1, description="The note content")


class MarkDoneRequest(BaseModel):
    """Request model for marking an action item as done/undone."""
    done: bool = Field(default=True, description="Whether the action item is completed")


# Response Schemas
class ActionItemResponse(BaseModel):
    """Response model for a single action item."""
    id: int
    text: str
    note_id: Optional[int] = None
    done: bool = False
    created_at: Optional[str] = None

    class Config:
        from_attributes = True  # Allows creation from SQLite Row objects


class ExtractResponse(BaseModel):
    """Response model for extraction endpoint."""
    note_id: Optional[int] = None
    items: List[ActionItemResponse]


class NoteResponse(BaseModel):
    """Response model for a note."""
    id: int
    content: str
    created_at: str

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str
    status_code: int = 400
