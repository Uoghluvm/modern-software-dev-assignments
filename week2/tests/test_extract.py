import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# TODO 2: Unit tests for LLM-powered extraction
class TestExtractActionItemsLLM:
    """Unit tests for extract_action_items_llm() function."""

    def test_llm_extract_bullet_list(self):
        """Test extraction from bullet-point list."""
        text = """
        Project tasks:
        - [ ] Set up database
        - [ ] Implement API endpoint
        - [ ] Write documentation
        """
        items = extract_action_items_llm(text)
        
        # LLM should extract all action items
        assert len(items) >= 3
        # Check that common action items are extracted (case-insensitive partial match)
        items_lower = [item.lower() for item in items]
        assert any("database" in item for item in items_lower)
        assert any("api" in item or "endpoint" in item for item in items_lower)
        assert any("documentation" in item or "document" in item for item in items_lower)

    def test_llm_extract_keyword_prefixed(self):
        """Test extraction from keyword-prefixed lines (TODO, Action, Next)."""
        text = """
        Meeting notes:
        TODO: Call the client
        Action: Review pull request
        Next: Update the roadmap
        """
        items = extract_action_items_llm(text)
        
        # Should extract all keyword-prefixed items
        assert len(items) >= 3
        items_lower = [item.lower() for item in items]
        assert any("client" in item or "call" in item for item in items_lower)
        assert any("pull request" in item or "review" in item for item in items_lower)
        assert any("roadmap" in item or "update" in item for item in items_lower)

    def test_llm_extract_empty_input(self):
        """Test that empty input returns empty list."""
        assert extract_action_items_llm("") == []
        assert extract_action_items_llm("   ") == []
        assert extract_action_items_llm("\n\n") == []

    def test_llm_extract_mixed_format(self):
        """Test extraction from mixed format notes."""
        text = """
        Project standup:
        - [ ] Fix login bug
        TODO: Deploy to staging
        * Test the new feature
        We should also update the README file.
        """
        items = extract_action_items_llm(text)
        
        # Should extract multiple action items
        assert len(items) >= 3
        items_lower = [item.lower() for item in items]
        assert any("login" in item or "bug" in item for item in items_lower)
        assert any("deploy" in item or "staging" in item for item in items_lower)
        assert any("test" in item or "feature" in item for item in items_lower)

    def test_llm_extract_narrative_text(self):
        """Test extraction from narrative text without explicit markers."""
        text = """
        We need to finalize the budget report by Friday.
        Should schedule a team meeting next week.
        Remember to send the invoice to the client.
        """
        items = extract_action_items_llm(text)
        
        # LLM should identify action items even without markers
        assert len(items) > 0
        items_lower = [item.lower() for item in items]
        # At least some action items should be extracted
        assert any("budget" in item or "report" in item for item in items_lower) or \
               any("meeting" in item or "schedule" in item for item in items_lower) or \
               any("invoice" in item or "client" in item for item in items_lower)

    def test_llm_extract_no_duplicates(self):
        """Test that duplicate action items are removed."""
        text = """
        - [ ] Buy groceries
        - buy groceries
        TODO: Buy groceries
        """
        items = extract_action_items_llm(text)
        
        # Should deduplicate (case-insensitive)
        items_lower = [item.lower() for item in items]
        grocery_count = sum(1 for item in items_lower if "groceries" in item or "grocery" in item)
        assert grocery_count == 1

    def test_llm_extract_only_narrative(self):
        """Test extraction from purely narrative text with no clear action items."""
        text = """
        The weather is nice today.
        Yesterday was a productive day.
        The team is working well together.
        """
        items = extract_action_items_llm(text)
        
        # Should return empty or very few items since there are no clear action items
        # LLM might extract nothing or be lenient - we just check it doesn't crash
        assert isinstance(items, list)
