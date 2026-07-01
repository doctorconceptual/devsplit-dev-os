# DevSplit Laravel Engineering Handbook

**Document:** Architecture
**Version:** 1.0.0
**Status:** Active

---

# Purpose

This document defines the architectural principles used by DevSplit when building Laravel applications.

It focuses on maintainability, scalability, readability, and long-term evolution rather than framework-specific implementation details.

---

# Architectural Philosophy

Laravel is a framework.

It is not an application architecture.

DevSplit builds a consistent architecture on top of Laravel to ensure every project is:

- Easy to understand
- Easy to maintain
- Easy to extend
- Easy to test
- Easy to scale

---

# Standard Application Flow

```
HTTP Request
      │
Middleware
      │
Form Request
      │
Controller
      │
Action
      │
Service
      │
Model
      │
Events / Jobs
      │
Resource / View
      │
Response
```

Every layer has one responsibility.

---

# Layer Responsibilities

## Controller

Coordinates the request.

Never contains business logic.

---

## Action

Represents one business use case.

Coordinates workflow.

---

## Service

Contains reusable business logic.

---

## Model

Represents persistence and relationships.

---

## Resource

Formats output.

---

# Design Principles

Prefer:

- Small classes
- Small methods
- Clear naming
- Dependency Injection
- Composition over inheritance
- Explicit dependencies

Avoid:

- God classes
- Fat controllers
- Hidden dependencies
- Circular dependencies
- Business logic inside models

---

# AI Notes

- Respect existing project architecture.
- Don't introduce new patterns without justification.
- Keep changes consistent with the existing codebase.

---

# Checklist

- Single responsibility?
- Correct layer?
- Existing architecture respected?
- No duplicated logic?
- Simple solution?