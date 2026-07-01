# DevSplit Laravel Engineering Handbook

**Document:** Code Review
**Version:** 1.0.0
**Status:** Active

---

# Purpose

This document defines how code reviews are performed at DevSplit.

The purpose of a code review is to improve software quality, maintainability, security, and long-term project health.

A code review is about improving the code—not criticizing the developer.

---

# Review Philosophy

Review every change as if you will be responsible for maintaining it for the next two years.

Focus on:

* Correctness
* Simplicity
* Maintainability
* Consistency
* Business value

Avoid reviewing based solely on personal preferences.

---

# Review Process

1. Understand the business requirement.
2. Review the existing implementation.
3. Examine the proposed changes.
4. Consider architectural impact.
5. Consider side effects.
6. Review testing.
7. Provide constructive feedback.
8. Approve only when confident.

---

# Review Categories

## Business Logic

Verify that:

* The correct problem is solved.
* Business rules are implemented correctly.
* Edge cases are considered.

---

## Architecture

Verify that:

* The correct layers are used.
* Responsibilities remain clear.
* Existing architecture is respected.

---

## Readability

Verify that:

* Code is easy to understand.
* Names are meaningful.
* Methods remain focused.
* Complexity is reasonable.

---

## Maintainability

Verify that:

* There is no unnecessary duplication.
* Existing code is reused where appropriate.
* The solution is easy to extend.

---

## Security

Review:

* Validation
* Authentication
* Authorization
* Sensitive data handling
* Input sanitization

---

## Performance

Review:

* Database queries
* N+1 issues
* Expensive loops
* External API calls
* Queue opportunities

Optimize only when necessary.

---

## Testing

Verify:

* Existing tests still pass.
* New functionality is tested where appropriate.
* Important scenarios are covered.
* Regression risks have been considered.

---

# Severity Levels

## Critical

Must be resolved before approval.

Examples:

* Security vulnerabilities
* Data loss
* Incorrect business logic
* Regressions

---

## Major

Should be resolved before approval.

Examples:

* Architectural violations
* Missing validation
* Missing authorization
* Missing tests for critical functionality

---

## Minor

Can be improved.

Examples:

* Naming
* Readability
* Documentation
* Minor refactoring

---

## Suggestion

Optional improvement that does not block approval.

---

# Giving Feedback

Feedback should be:

* Respectful
* Specific
* Actionable
* Supported by reasoning

Explain **why** a change is recommended.

Whenever practical, suggest an improved approach rather than only identifying a problem.

---

# Best Practices

* Review the entire change, not only modified lines.
* Understand the context before commenting.
* Consider long-term maintainability.
* Separate required changes from optional improvements.

---

# Common Mistakes

* Reviewing style instead of correctness.
* Missing regressions outside the changed files.
* Approving without understanding the requirement.
* Requesting unnecessary refactoring.
* Ignoring business impact.

---

# AI Notes

When reviewing code:

* Review the surrounding code, not only the diff.
* Consider downstream effects.
* Look for regressions outside the immediate change.
* Distinguish required fixes from optional suggestions.
* Do not recommend large architectural refactors unless they are directly related to the task.

---

# Final Review Checklist

Before approving:

* Requirements satisfied.
* Existing functionality preserved.
* Architecture respected.
* Security considered.
* Performance acceptable.
* Tests adequate.
* Documentation updated where required.
* Ready for production.

---

**End of Code Review**
