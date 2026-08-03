# Volume 3 – System Architecture

**Project:** AI-Powered Smart Campus Attendance Management Platform  
**Version:** 1.0 (Architecture Locked)

**Purpose:** This document converts the approved requirements (Volume 2) into a complete system architecture. It defines how the system will be built, without implementation code. It is derived from the approved BRS and Locked SRS.

# Architecture Philosophy

Before designing anything, we define a few architectural principles.

This project will not be built as another college project.

It will be built like an enterprise SaaS application.

Every architectural decision must satisfy these goals:

- Scalability
- Maintainability
- Security
- Performance
- Testability
- Modularity
- Future AI Expansion
- Multi-Institution Readiness

# Part 1 — High-Level System Architecture

## 1.1 Overall Architecture

```text
                    Users
        ┌────────────┼────────────┐
        │            │            │
 Super Admin    Faculty      Students
        │            │            │
        └────────────┼────────────┘
                     │
              React Frontend (SPA)
                     │
        ─────────────────────────────
              HTTPS + JWT
        ─────────────────────────────
                     │
          Django REST API Gateway
                     │
     ┌───────────────┼────────────────┐
     │               │                │
Authentication   Business APIs   AI Services
     │               │                │
     └───────────────┼────────────────┘
                     │
            Business Service Layer
                     │
     ┌───────────────┼─────────────────────┐
     │               │                     │
 PostgreSQL      Redis Cache        Celery Workers
     │                                   │
     └───────────────────────────────────┘
                     │
             Face Recognition Engine
                     │
                 OpenCV + AI Models
```

### Why this architecture?

Unlike the existing project where everything lived inside Flask routes, responsibilities are separated into dedicated layers.

Benefits:

- Easier maintenance
- Independent frontend/backend
- Better testing
- Easier scaling
- Cleaner codebase
- Future mobile app support

## 1.2 Logical Layers

The system will consist of eight logical layers.

### Layer 1 – Presentation Layer

**Technology**

- React
- Tailwind CSS
- shadcn/ui

**Responsibilities**

- UI
- Forms
- Dashboards
- Navigation
- Client-side validation

No business logic should exist here.

### Layer 2 – API Layer

**Technology**

- Django REST Framework

**Responsibilities**

- Receive HTTP requests
- Authentication
- Validation
- Serialization
- Response formatting

### Layer 3 – Business Layer

**Responsibilities**

Contains all business rules.

Examples:

- Attendance rules
- Duplicate checking
- Role permissions
- Report generation
- Student workflows

This is the heart of the application.

### Layer 4 – AI Layer

**Responsibilities**

- Face recognition
- Attendance prediction
- OCR
- AI summaries
- Analytics
- AI assistant

Designed as a separate layer so AI features can evolve independently.

### Layer 5 – Data Access Layer

**Responsibilities**

- Database interaction
- Query optimization
- Transactions
- Data integrity

### Layer 6 – Database Layer

**Technology**

- PostgreSQL

**Responsibilities**

- Persistent storage
- Relationships
- Constraints
- Indexes
- Audit records

### Layer 7 – Background Processing

**Technology**

- Celery
- Redis

**Responsibilities**

- Email sending
- Report generation
- AI processing
- Long-running jobs
- Scheduled tasks

### Layer 8 – Infrastructure Layer

Includes:

- Docker
- Nginx
- Logging
- Monitoring
- Environment configuration

# Part 2 — Backend Architecture

## Why Django?

Compared to the existing Flask application, Django provides:

- Mature authentication
- ORM
- Admin capabilities
- Security features
- Scalability
- Rich ecosystem

## Backend Folder Philosophy

Instead of organizing by technical type alone, we organize around business modules.

```text
backend/
│
├── config/
├── apps/
│
├── authentication/
├── users/
├── institutions/
├── departments/
├── faculty/
├── students/
├── academic/
├── attendance/
├── face_recognition/
├── reports/
├── dashboard/
├── notifications/
├── ai/
├── audit/
└── common/
```

### Why Modular Apps?

Each app owns:

- Models
- APIs
- Business logic
- Permissions
- Validation
- Tests

Benefits:

- Low coupling
- High cohesion
- Easier maintenance
- Independent development

## Backend Request Flow

```text
Request

↓

URL Router

↓

Authentication

↓

Permission Check

↓

API View

↓

Serializer

↓

Business Service

↓

Database

↓

Response
```

Every request follows exactly this path.

## Cross-Cutting Components

Every module shares:

- Authentication
- Authorization
- Logging
- Exception Handling
- Validation
- Audit Logging
- Response Formatting

This avoids duplicate implementations.

# Part 3 — Frontend Architecture

## Frontend Philosophy

React should behave like a client application, not like a server-rendered website.

## Folder Structure

```text
src/

assets/
components/
layouts/
pages/
features/
hooks/
services/
context/
routes/
utils/
constants/
styles/
```

### Why Feature-Based Organization?

Instead of placing every page in a single folder, each feature owns its related UI.

Example:

```text
attendance/

AttendancePage

AttendanceTable

AttendanceFilters

AttendanceCharts

AttendanceServices
```

Benefits:

- Easier maintenance
- Better scalability
- Cleaner code

## Frontend Layers

### UI Components

Reusable components.

Examples:

- Button
- Modal
- Table
- Form
- Card
- Badge

### Feature Components

Business-specific components.

Examples:

- Student Table
- Attendance Session
- Face Registration Form

### Pages

Route-level screens.

Examples:

- Dashboard
- Login
- Students
- Attendance
- Reports

### Services

Responsible for API communication only.

No UI logic.

No business rules.

### Context / State

Responsibilities:

- Authentication state
- Current user
- Theme
- Notifications

## Frontend Navigation

```text
Login

↓

Dashboard

↓

Modules

↓

CRUD

↓

Reports

↓

Analytics

↓

Settings
```

## Frontend Layouts

The application will use dedicated layouts instead of one universal page.

Examples:

- Authentication Layout
- Dashboard Layout
- Student Portal Layout
- Faculty Layout

This keeps responsibilities separated and supports different experiences per role.

# Part 4 — Database Architecture

## Database Philosophy

The database is the system's single source of truth.

Business rules should be reinforced through relationships and constraints where appropriate.

## Core Entities

- Institution
- Department
- Faculty
- Student
- Course
- Subject
- Class
- Attendance
- AttendanceSession
- FaceEncoding
- Report
- Notification
- AuditLog
- User
- Role

These entities align with the BRS scope and the approved SRS.

## High-Level Entity Relationship

```text
Institution
      │
      ├──────────────┐
      │              │
Department        Users
      │              │
      │              ├─────────┐
      │              │         │
 Faculty         Student     Admin
      │              │
      └──────┬───────┘
             │
         Attendance
             │
      Attendance Session
             │
       Face Encoding
```

This is a conceptual relationship diagram. Detailed tables and cardinalities will be finalized in the Database Design phase.

## Database Principles

### Normalization

Target:

Third Normal Form (3NF)

Avoid:

- Duplicate student data
- Repeated attendance data
- Repeated department names

### Primary Keys

Every table uses a surrogate primary key (e.g., UUID or integer strategy to be finalized later).

### Foreign Keys

Relationships enforce integrity.

Examples:

- Student → Institution
- Student → Department
- Attendance → Student
- Attendance → Class

### Constraints

The database should prevent:

- Duplicate attendance
- Invalid foreign references
- Orphan records

Additional constraints will be defined during the detailed database design.

### Index Strategy

Expected indexes include:

- Student ID
- Attendance Date
- Class ID
- Department ID
- User Email

The exact indexing plan will be documented alongside the physical schema.

## Database Categories

### Master Data

Rarely changes.

Examples:

- Departments
- Courses
- Subjects
- Roles

### Transaction Data

Changes daily.

Examples:

- Attendance
- Reports
- Notifications

### Security Data

Examples:

- Users
- Tokens
- Audit Logs

### AI Data

Examples:

- Face Encodings
- AI Predictions
- OCR Results
- AI Summaries

# Part 5 — Architectural Principles

## Separation of Concerns

Every layer has one responsibility.

```text
UI

↓

API

↓

Business Logic

↓

Database
```

## Low Coupling

Modules should not depend heavily on one another.

Example:

Attendance should not directly manipulate Student internals; it should interact through well-defined interfaces.

## High Cohesion

Each module owns one business capability.

Example:

Attendance module

- Attendance
- Attendance History
- Attendance Session

Nothing unrelated.

## API First

Frontend never accesses the database.

```text
Frontend

↓

REST API

↓

Backend

↓

Database
```

This enables future mobile clients and third-party integrations.

## Security by Design

Security is built into the architecture rather than added afterward.

Key architectural elements include:

- JWT Authentication
- RBAC
- Input validation
- Audit logging
- Secure configuration
- Principle of least privilege

## Future Scalability

The architecture is intentionally designed to support future enhancements identified in the BRS, such as:

- Multi-institution deployment
- AI expansion
- Mobile applications
- Background processing
- Horizontal scaling

### Architecture Decision Summary (ADR)

| Decision | Choice | Reason |
|---|---|---|
| Frontend | React SPA | Decoupled UI and reusable components |
| Backend | Django + DRF | Mature ecosystem, security, REST APIs |
| Database | PostgreSQL | Strong relational integrity and scalability |
| Authentication | JWT | Stateless, API-friendly authentication |
| Background Jobs | Celery + Redis | Asynchronous processing |
| Architecture Style | Layered Modular Monolith | Simpler than microservices while remaining highly maintainable |
| API Style | REST | Matches project scope and frontend needs |
| Deployment | Docker Containers | Consistent development and production environments |

# Volume 3 Approval Summary

## Deliverables Completed

- ✅ High-Level System Architecture
- ✅ Layered Architecture Definition
- ✅ Backend Architecture
- ✅ Backend Module Organization
- ✅ Frontend Architecture
- ✅ Frontend Folder and Feature Strategy
- ✅ Conceptual Database Architecture
- ✅ High-Level Entity Relationships
- ✅ Architectural Principles
- ✅ Architecture Decision Record (ADR)

## Architecture Status

The solution architecture is now defined at a high level and is consistent with the approved BRS and Locked SRS. Detailed physical database schema, API specifications, and individual module designs will build on this foundation without changing its core structure.
