"""
TODO 3 Refactored: Action Items Router with proper API schemas and error handling.
"""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm
from ..schemas import (
    ExtractRequest,
    ExtractResponse,
    ActionItemResponse,
    MarkDoneRequest,
)


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse, status_code=status.HTTP_200_OK)
def extract(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using rule-based heuristics.
    
    Args:
        request: ExtractRequest containing text and save_note flag
    
    Returns:
        ExtractResponse with extracted action items and optional note_id
        
    Raises:
        HTTPException: If text is empty or extraction fails
    """
    try:
        # Extract action items using rule-based method
        items = extract_action_items(request.text)
        
        # Optionally save the note
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)
        
        # Insert action items into database
        item_ids = db.insert_action_items(items, note_id=note_id)
        
        # Build response
        action_items = [
            ActionItemResponse(id=item_id, text=text, note_id=note_id)
            for item_id, text in zip(item_ids, items)
        ]
        
        return ExtractResponse(note_id=note_id, items=action_items)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract action items: {str(e)}"
        )


# TODO 4: LLM-powered extraction endpoint
@router.post("/extract-llm", response_model=ExtractResponse, status_code=status.HTTP_200_OK)
def extract_llm(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using LLM (Ollama).
    
    This endpoint uses an LLM to extract action items, which can better
    understand context and identify action items from narrative text.
    
    Args:
        request: ExtractRequest containing text and save_note flag
    
    Returns:
        ExtractResponse with extracted action items and optional note_id
        
    Raises:
        HTTPException: If text is empty or extraction fails
    """
    try:
        # Extract action items using LLM
        items = extract_action_items_llm(request.text)
        
        # Optionally save the note
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)
        
        # Insert action items into database
        item_ids = db.insert_action_items(items, note_id=note_id)
        
        # Build response
        action_items = [
            ActionItemResponse(id=item_id, text=text, note_id=note_id)
            for item_id, text in zip(item_ids, items)
        ]
        
        return ExtractResponse(note_id=note_id, items=action_items)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract action items with LLM: {str(e)}"
        )


@router.get("", response_model=List[ActionItemResponse])
def list_all(note_id: Optional[int] = None) -> List[ActionItemResponse]:
    """
    List all action items, optionally filtered by note_id.
    
    Args:
        note_id: Optional note ID to filter action items
        
    Returns:
        List of ActionItemResponse objects
    """
    try:
        rows = db.list_action_items(note_id=note_id)
        return [
            ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve action items: {str(e)}"
        )


@router.post("/{action_item_id}/done", response_model=ActionItemResponse)
def mark_done(action_item_id: int, request: MarkDoneRequest) -> ActionItemResponse:
    """
    Mark an action item as done or undone.
    
    Args:
        action_item_id: The ID of the action item to update
        request: MarkDoneRequest with done status
        
    Returns:
        ActionItemResponse with updated status
        
    Raises:
        HTTPException: If action item not found or update fails
    """
    try:
        db.mark_action_item_done(action_item_id, request.done)
        
        # Return minimal response (could be enhanced to fetch full item)
        return ActionItemResponse(
            id=action_item_id,
            text="",  # Not fetched for efficiency
            done=request.done
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update action item: {str(e)}"
        )

