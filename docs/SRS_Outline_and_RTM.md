# Volume 2 – Locked Software Requirements Specification (SRS) + Requirement Traceability Matrix (RTM)

**Project:** AI-Powered Smart Campus Attendance Management Platform  
**Version:** 1.0 (Locked for Design & Development)

**Source of Truth:** This SRS is derived directly from the approved Business Requirements Specification (BRS). Where implementation details are not explicitly defined in the BRS, they are intentionally left for later design documents rather than assumed.

# Purpose of Volume 2

The Business Requirements Specification (BRS) defines what the business needs.

The Software Requirements Specification (SRS) defines what the software must do to satisfy those business needs.

After approval, this document becomes the development contract.

Any future feature request will be treated as a change request rather than silently added.

# Part 1 – System Overview

## 1.1 System Name

AI-Powered Smart Campus Attendance Management Platform

## 1.2 System Type

Web-based enterprise application.

## 1.3 Target Users

- Super Administrator
- Institution Administrator
- Faculty
- Student

These user roles are defined in the BRS.

## 1.4 System Purpose

The platform shall:

- Automate attendance using facial recognition.
- Prevent proxy attendance.
- Manage institutional academic data.
- Provide attendance analytics.
- Generate reports.
- Support multiple user roles.
- Provide AI-powered operational insights.

## 1.5 System Scope

The system shall support:

- Authentication
- Authorization
- Student Management
- Faculty Management
- Department Management
- Class Management
- Face Registration
- Attendance
- Reporting
- Analytics
- Notifications
- Audit Logging
- AI Services

These functional areas are within the scope defined by the BRS.

# Part 2 – Actors

| Actor | Description |
|---|---|
| Super Administrator | Global platform management |
| Institution Administrator | Institution operations |
| Faculty | Attendance management |
| Student | Attendance viewing |

# Part 3 – Functional Requirements (Locked)

Each requirement is assigned a permanent identifier for traceability.

## FR-001 – Authentication

The system shall provide secure user authentication.

### Includes

- Login
- Logout
- JWT Authentication
- Password Reset
- Email Verification
- Session Management

## FR-002 – User Management

The system shall support:

- User creation
- User modification
- User activation/deactivation
- Profile management
- Role assignment

## FR-003 – Student Management

The system shall support:

- Student registration
- Student profile updates
- Enrollment management

## FR-004 – Faculty Management

The system shall support:

- Faculty CRUD
- Department assignment
- Faculty profile management

## FR-005 – Department Management

The system shall support:

- Department CRUD
- Department hierarchy (if introduced in future design)

**Note:** The BRS specifies CRUD operations and mentions department hierarchy; detailed hierarchy behavior will be defined during database and module design.

## FR-006 – Academic Structure

The system shall support:

- Academic years
- Courses
- Sections
- Subjects
- Classes

## FR-007 – Face Registration

The system shall support:

- Face enrollment
- Face validation
- Duplicate face detection
- Face encoding storage

## FR-008 – Attendance

The system shall support:

- Attendance session initiation
- Automatic attendance
- Attendance history
- Attendance search
- Manual correction workflow
- Bulk attendance operations

## FR-009 – Dashboard

The system shall display:

- KPIs
- Live attendance
- Charts
- Alerts
- Institution statistics

## FR-010 – Reporting

The system shall provide:

- Daily reports
- Weekly reports
- Monthly reports
- Department reports
- Student reports
- Faculty reports
- Excel export
- PDF export

## FR-011 – Notifications

The system shall notify users of relevant attendance- and system-related events.

The BRS includes notifications within project scope but does not define delivery mechanisms. Notification channels will therefore be specified later in the design phase.

## FR-012 – AI Services

The platform shall support AI capabilities including:

- Attendance insights
- Trend prediction
- At-risk student identification
- AI-generated attendance summaries
- Natural language report querying
- OCR for student identity documents
- Duplicate face detection
- Administrative AI assistant

## FR-013 – Audit Logging

The system shall record audit logs for sensitive administrative actions.

# Part 4 – Non-Functional Requirements (Locked)

## Performance

- Standard API response target: under 500 ms.
- Support concurrent users.
- Optimize database queries.

## Scalability

The system shall support:

- Horizontal scaling
- Modular architecture
- Multi-tenant readiness

## Security

The system shall implement:

- JWT authentication
- Password hashing
- HTTPS
- RBAC
- Input validation
- Rate limiting
- Audit logging

## Reliability

The system shall support:

- High availability
- Automated backups
- Error recovery

## Maintainability

The system shall be designed with:

- Layered architecture
- Clean code principles
- Documentation
- Automated testing

These non-functional requirements are defined in the BRS.

# Part 5 – Business Rules (Locked)

| ID | Rule |
|---|---|
| BR-001 | Every student belongs to one institution. |
| BR-002 | Every faculty member belongs to one department. |
| BR-003 | Attendance can only be marked for scheduled classes. |
| BR-004 | Duplicate attendance records are prohibited. |
| BR-005 | Face registration requires administrator approval. |
| BR-006 | Attendance modifications must be audited. |
| BR-007 | Users may access only data permitted by their roles. |

These rules are directly sourced from the BRS.

# Part 6 – Constraints

The solution shall use the mandatory technology stack defined by the BRS:

- React.js
- Tailwind CSS
- Django
- Django REST Framework
- PostgreSQL
- Python
- Docker

Preferred supporting technologies include Redis, Celery, Nginx, and GitHub Actions.

# Part 7 – Assumptions

The following assumptions are inherited from the BRS:

- Institutions have camera-enabled devices.
- Stable internet is available.
- Users possess institutional credentials.
- Face recognition performs adequately under normal conditions.

# Part 8 – Risks

The following project risks are identified:

- Poor lighting affecting recognition.
- Camera hardware limitations.
- Large biometric datasets.
- Network outages.
- User resistance to change.

Dependencies include camera hardware, face-recognition libraries, PostgreSQL, Docker, email services, and AI providers where applicable.

# Part 9 – Acceptance Criteria

The project shall be considered complete when it:

- Automates attendance reliably.
- Prevents duplicate attendance.
- Provides accurate reporting.
- Supports all defined user roles.
- Demonstrates secure architecture.
- Is deployable using Docker.
- Meets the portfolio and pilot-deployment objectives stated in the BRS.

# Part 10 – Requirement Traceability Matrix (RTM)

The RTM ensures every requirement is mapped through design, implementation, and testing.

| Requirement | Module | Database | API | Frontend | Testing |
|---|---|---|---|---|---|
| FR-001 Authentication | Auth | Users, Tokens | Auth API | Login UI | Auth Tests |
| FR-002 User Management | Users | Users, Roles | User API | User Management | CRUD Tests |
| FR-003 Student Management | Students | Students | Student API | Student UI | CRUD Tests |
| FR-004 Faculty Management | Faculty | Faculty | Faculty API | Faculty UI | CRUD Tests |
| FR-005 Department Management | Departments | Departments | Department API | Department UI | CRUD Tests |
| FR-006 Academic Structure | Academic | Courses, Subjects, Classes | Academic API | Academic UI | Validation Tests |
| FR-007 Face Registration | Face | Face Encodings | Face API | Face Registration UI | Recognition Tests |
| FR-008 Attendance | Attendance | Attendance | Attendance API | Attendance UI | Workflow Tests |
| FR-009 Dashboard | Dashboard | Analytics Views | Dashboard API | Dashboard | UI & KPI Tests |
| FR-010 Reporting | Reports | Attendance Data | Report API | Report UI | Export Tests |
| FR-011 Notifications | Notifications | Notification Records | Notification API | Notification Center | Delivery Tests |
| FR-012 AI Services | AI | AI-related Data | AI API | AI Dashboard | AI Feature Tests |
| FR-013 Audit Logging | Audit | Audit Logs | Audit API | Audit Viewer | Audit Tests |

# Part 11 – Requirement Coverage Summary

## Core Business

- Authentication ✔
- Attendance ✔
- Face Recognition ✔
- Reports ✔
- Dashboards ✔

## Administration

- User Management ✔
- Departments ✔
- Faculty ✔
- Students ✔
- Academic Structure ✔

## Enterprise Features

- RBAC ✔
- JWT ✔
- Audit Logging ✔
- AI Services ✔
- Analytics ✔
- Exporting ✔
- Multi-role Support ✔

# Part 12 – SRS Lock Statement

The following artifacts are now considered locked unless formally revised:

- Functional Requirements (FR-001 to FR-013)
- Business Rules (BR-001 to BR-007)
- Non-Functional Requirements
- User Roles
- Acceptance Criteria
- Requirement Traceability Matrix
- Project Scope

Any future additions—such as new modules, workflows, or integrations—should be evaluated as change requests to preserve architectural consistency.

# Volume 2 Approval Summary

## Deliverables Completed

- ✅ Locked Software Requirements Specification (SRS)
- ✅ Functional Requirements Catalog
- ✅ Non-Functional Requirements Catalog
- ✅ Business Rules Register
- ✅ Constraints, Assumptions, Risks, and Acceptance Criteria
- ✅ Requirement Traceability Matrix (RTM)
- ✅ Requirements Lock Statement
