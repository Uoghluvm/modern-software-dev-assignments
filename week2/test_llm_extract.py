#!/usr/bin/env python3
"""Quick test script for LLM-based action item extraction."""

from week2.app.services.extract import extract_action_items_llm


# Test cases
test_notes = """
- [ ] Buy milk and eggs
- Call dentist to schedule appointment
TODO: Finish the weekly report
Action: Review code changes
Next: Update documentation

Meeting notes:
We need to implement the new feature by Friday.
Should also fix the bug in the login page.
"""

print("Testing LLM-based extraction...")
print("=" * 60)
print("Input notes:")
print(test_notes)
print("=" * 60)

try:
    result = extract_action_items_llm(test_notes)
    print(f"\nExtracted {len(result)} action items:")
    for i, item in enumerate(result, 1):
        print(f"{i}. {item}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
