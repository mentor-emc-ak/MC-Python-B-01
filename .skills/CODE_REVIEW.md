# Python Code Review Skill

## Objective

Review all Python code against production-quality standards before considering the task complete.

## Review Categories

### 1. Readability

* Clear and descriptive names
* Consistent naming conventions
* Readable control flow
* Minimal nesting
* No unnecessary comments
* No ambiguous abbreviations

### 2. Structure

* Single responsibility per function
* Single responsibility per class
* Logical module organization
* No excessively large functions
* No duplicated logic
* Proper separation of concerns

### 3. Type Safety

* Type hints present
* Accurate return types
* Accurate parameter types
* Consistent typing throughout code

### 4. Documentation

* Public functions documented
* Public classes documented
* Complex business logic explained
* Documentation matches implementation

### 5. Error Handling

* Specific exceptions used
* No broad exception catching unless justified
* No silent failures
* Meaningful error messages
* Failure scenarios considered

### 6. Logging

* Logging used where appropriate
* No print statements
* Appropriate log levels
* Useful operational context in logs

### 7. Testing

* Happy path covered
* Edge cases covered
* Failure cases covered
* Regression risks identified
* Existing tests remain valid

### 8. Performance

* No unnecessary loops
* No repeated expensive operations
* Appropriate data structures selected
* Avoidable complexity removed

### 9. Security

* No hardcoded secrets
* Input validation present
* Sensitive information protected
* Safe handling of external inputs

### 10. Configuration

* Environment-specific values externalized
* No hardcoded credentials
* No hardcoded endpoints without justification
* Configurable parameters extracted

### 11. Maintainability

* DRY principle followed
* Reusable components preferred
* Low complexity
* Future modifications are straightforward

### 12. Code Hygiene

* No unused imports
* No dead code
* No commented-out code
* No debug statements
* No temporary workarounds left behind

## Review Output Format

For every review, provide:

### Passes

* List standards already met

### Issues

* List findings grouped by category

### Severity

* Critical
* Major
* Minor
* Suggestion

### Final Score

* Readability: /10
* Structure: /10
* Type Safety: /10
* Error Handling: /10
* Testing: /10
* Maintainability: /10
* Overall: /10

### Approval Status

* Approved
* Approved with Minor Suggestions
* Changes Required
* Major Rework Required

## Completion Rule

Do not approve code if any of the following exist:

* Hardcoded secrets
* Missing error handling for critical operations
* Significant duplicated logic
* Dead code
* Unused imports
* Missing tests for new functionality
* Broad exception handling without justification
* Critical security concerns
