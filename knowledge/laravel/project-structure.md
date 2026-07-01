# Laravel Project Structure

## Request Lifecycle
Request → Middleware → FormRequest → Controller → Action → Service → Model → Events → Jobs → Response

## Standard Folders
Actions/
AI/
Contracts/
DTOs/
Enums/
Events/
Exceptions/
Http/
Integrations/
Jobs/
Listeners/
Mail/
Models/
Notifications/
Observers/
Policies/
Providers/
Rules/
Services/
Traits/
ValueObjects/

## Responsibilities
Controller: orchestration only.
Action: one business use case.
Service: business logic.
Model: persistence.
DTO: structured data.
Job: async work.
Event: system notification.
Policy: authorization.

## AI Notes
- Follow existing project conventions first.
- Don't move files during feature work.
- Suggest structural improvements separately.

## Checklist
- Correct layer?
- Single responsibility?
- Existing functionality preserved?
- Tests considered?
