# Test Coverage Report

Run the test suite with coverage analysis and provide actionable insights.

## Instructions

1. **Run tests with coverage**:

   ```bash
   cd week4
   PYTHONPATH=. pytest -q backend/tests --cov=backend/app --cov-report=term-missing --maxfail=1 -x
   ```

2. **Analyze the results**:
   - If tests fail:
     - Show the failing test details
     - Suggest potential fixes based on the error message
     - Recommend next steps (e.g., check specific files, run single test)
   - If tests pass:
     - Show coverage percentage for each module
     - Identify files with coverage below 80%
     - Suggest specific lines that need test coverage

3. **Provide a summary**:
   - Total coverage percentage
   - Number of tests passed/failed
   - Top 3 priority areas for improving coverage
   - Recommended next actions

## Safety Notes

- This command only reads and analyzes; it doesn't modify code
- Safe to run at any time
- If tests fail with `-x` flag, execution stops at first failure
