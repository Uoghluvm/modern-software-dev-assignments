from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# TODO 1: LLM-powered extraction using Ollama
# Import Pydantic for structured outputs
from pydantic import BaseModel


class ActionItemsResponse(BaseModel):
    """Pydantic model for structured output from Ollama."""
    action_items: List[str]


def extract_action_items_llm(text: str, model: str = "llama3.1:8b") -> List[str]:
    """
    Extract action items from text using an LLM (Ollama).
    
    This function uses Ollama's structured output capability to ensure
    the LLM returns a JSON array of action items.
    
    Args:
        text: The input notes/text to extract action items from
        model: The Ollama model to use (default: llama3.1:8b)
    
    Returns:
        A list of extracted action item strings
    """
    if not text or not text.strip():
        return []
    
    # System prompt to guide the LLM
    system_prompt = """You are an AI assistant that extracts action items from free-form notes.
Your task is to:
1. Identify all actionable tasks, to-dos, and action items in the provided text
2. Extract them as clear, concise action items
3. Remove bullet points, checkboxes, or prefixes like "TODO:", "Action:", etc.
4. Return only the core action item text
5. If there are no action items, return an empty list

Examples:
- "- [ ] Buy groceries" → "Buy groceries"
- "TODO: Call the dentist" → "Call the dentist"
- "Need to finish the report by Friday" → "Finish the report by Friday"
"""
    
    try:
        # Use Ollama chat with structured output
        response = chat(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': f"Extract all action items from the following notes:\n\n{text}"
                }
            ],
            format=ActionItemsResponse.model_json_schema(),  # Structured output
        )
        
        # Parse the response
        message_content = response.message.content
        
        # Parse JSON response
        result = json.loads(message_content)
        action_items = result.get('action_items', [])
        
        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: List[str] = []
        for item in action_items:
            item_stripped = item.strip()
            lowered = item_stripped.lower()
            if lowered and lowered not in seen:
                seen.add(lowered)
                unique.append(item_stripped)
        
        return unique
        
    except Exception as e:
        # Fallback to rule-based extraction on error
        print(f"LLM extraction failed: {e}. Falling back to rule-based extraction.")
        return extract_action_items(text)
