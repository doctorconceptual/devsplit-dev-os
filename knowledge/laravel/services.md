# DevSplit Laravel Engineering Handbook

**Document:** Services

---

# Purpose

Services contain reusable business logic.

---

# Responsibilities

Services own:

- Business rules
- Calculations
- External integrations
- Complex workflows

---

# Avoid

Services should never:

- Handle HTTP
- Validate requests
- Return Responses
- Render views

---

# Naming

```
InvoiceService

PricingService

TaxService
```

---

# Best Practices

- Keep methods focused.
- Inject dependencies.
- Avoid static methods unless justified.
- Prefer composition.

---

# Common Mistakes

❌ Validation inside Services

❌ Returning JSON

❌ Massive service classes

---

# AI Notes

Before creating a new Service:

Check whether similar business logic already exists.

Reuse first.

---

# Checklist

✓ Business logic only?

✓ Reusable?

✓ No presentation logic?

✓ No duplication?