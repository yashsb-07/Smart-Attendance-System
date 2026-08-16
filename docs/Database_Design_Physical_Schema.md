# Database Design / Physical Schema

**Project:** AI-Powered Smart Campus Attendance Management Platform  
**Version:** 1.0 (Database Design Phase)  
**Status:** Proposed for implementation approval  
**Database:** PostgreSQL  
**ORM:** Django ORM

---

## 1. Purpose

This document defines the physical relational database design required to implement the already-approved Smart Campus platform.

It is derived from the locked BRS, SRS + RTM, System Architecture, Module Specifications, API Strategy, Security Architecture, Deployment Architecture, and Complete Development Roadmap.

It does not introduce new business functionality or change the frozen architecture.

---

## 2. Decision Classification

### Requirement-derived

- Every student belongs to one institution.
- Every faculty member belongs to one department.
- Attendance can only be marked for scheduled classes.
- Duplicate attendance records are prohibited.
- Face registration requires administrator approval.
- Attendance modifications must be audited.
- Users may access only data permitted by their roles.
- Academic years, courses, subjects, sections, and classes are supported.

### Architecture-derived

- PostgreSQL.
- Relational integrity through foreign keys and constraints.
- Third Normal Form target.
- Surrogate primary keys.
- Indexed important query paths.
- Business-module ownership of database models.

### Physical implementation decisions

- Project-owned tables use BIGINT / Django BigAutoField surrogate keys.
- Master records that need historical references use controlled deactivation.
- Transaction and audit records are not physically deleted through normal workflows.
- Institution-scoped business identifiers use composite uniqueness where required.
- Foreign-key deletion behavior is conservative for historical data.

---

## 3. Global Conventions

- PostgreSQL tables use plural `snake_case`.
- Django models use singular PascalCase.
- Business tables use `created_at` and `updated_at` where lifecycle tracking is useful.
- Mandatory business relationships are represented by non-null foreign keys.
- `PROTECT` is preferred where deletion could invalidate historical data.
- `CASCADE` is reserved for true dependent records.
- `SET_NULL` is used only for optional historical references.

### Primary-key decision

The existing committed Accounts implementation already uses Django `BigAutoField`. The physical schema therefore standardizes project-owned tables on BIGINT / BigAutoField rather than introducing mixed UUID and integer strategies.

---

# 4. Physical Schema

## 4.1 Institution

**Table:** `institutions`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| name | VARCHAR(200) | No | — | |
| code | VARCHAR(50) | No | — | UNIQUE |
| description | TEXT | Yes | NULL | |
| email | VARCHAR(254) | Yes | NULL | |
| phone | VARCHAR(30) | Yes | NULL | |
| address | TEXT | Yes | NULL | |
| website | VARCHAR(255) | Yes | NULL | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Indexes: `code`, `is_active`.

Institution deletion is protected once dependent institutional data exists; normal administration uses deactivation.

---

## 4.2 InstitutionConfiguration

**Table:** `institution_configurations`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| institution_id | BIGINT | No | — | FK, UNIQUE |
| default_academic_year_id | BIGINT | Yes | NULL | FK |
| timezone | VARCHAR(64) | No | UTC | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

One institution has at most one configuration record.

---

## 4.3 InstitutionBranding

**Table:** `institution_branding`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| institution_id | BIGINT | No | — | FK, UNIQUE |
| logo_path | VARCHAR(500) | Yes | NULL | |
| primary_color | VARCHAR(20) | Yes | NULL | |
| secondary_color | VARCHAR(20) | Yes | NULL | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

File storage remains outside PostgreSQL.

---

## 4.4 Department

**Table:** `departments`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| institution_id | BIGINT | No | — | FK |
| name | VARCHAR(150) | No | — | |
| code | VARCHAR(50) | No | — | |
| description | TEXT | Yes | NULL | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(institution_id, code)`.

Indexes: `institution_id`, `(institution_id, is_active)`, `(institution_id, name)`.

This enforces the approved rule that every department belongs to one institution.

---

## 4.5 AcademicYear

**Table:** `academic_years`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| institution_id | BIGINT | No | — | FK |
| name | VARCHAR(50) | No | — | |
| start_date | DATE | No | — | |
| end_date | DATE | No | — | |
| is_current | BOOLEAN | No | FALSE | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(institution_id, name)`.

Check: `end_date > start_date`.

---

## 4.6 Course

**Table:** `courses`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| institution_id | BIGINT | No | — | FK |
| department_id | BIGINT | Yes | NULL | FK |
| name | VARCHAR(150) | No | — | |
| code | VARCHAR(50) | No | — | |
| description | TEXT | Yes | NULL | |
| duration_years | SMALLINT | Yes | NULL | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(institution_id, code)`.

---

## 4.7 Subject

**Table:** `subjects`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| course_id | BIGINT | No | — | FK |
| name | VARCHAR(150) | No | — | |
| code | VARCHAR(50) | No | — | |
| description | TEXT | Yes | NULL | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(course_id, code)`.

---

## 4.8 Section

**Table:** `sections`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| academic_year_id | BIGINT | No | — | FK |
| course_id | BIGINT | No | — | FK |
| name | VARCHAR(50) | No | — | |
| code | VARCHAR(50) | No | — | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(academic_year_id, course_id, code)`.

---

## 4.9 Class

**Table:** `classes`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| academic_year_id | BIGINT | No | — | FK |
| course_id | BIGINT | No | — | FK |
| subject_id | BIGINT | No | — | FK |
| section_id | BIGINT | No | — | FK |
| faculty_id | BIGINT | No | — | FK |
| name | VARCHAR(150) | No | — | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Indexes: academic year, course, subject, section, faculty.

Attendance sessions must reference a valid class.

---

## 4.10 Faculty

**Table:** `faculty`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| user_id | BIGINT | No | — | FK, UNIQUE |
| department_id | BIGINT | No | — | FK |
| employee_code | VARCHAR(50) | No | — | |
| designation | VARCHAR(100) | Yes | NULL | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(department_id, employee_code)`.

Every faculty member belongs to one department.

---

## 4.11 Student

**Table:** `students`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| user_id | BIGINT | Yes | NULL | FK, UNIQUE |
| institution_id | BIGINT | No | — | FK |
| department_id | BIGINT | No | — | FK |
| roll_number | VARCHAR(50) | No | — | |
| admission_number | VARCHAR(50) | Yes | NULL | |
| date_of_birth | DATE | Yes | NULL | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(institution_id, roll_number)`.

Every student belongs to one institution.

---

## 4.12 StudentEnrollment

**Table:** `student_enrollments`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| student_id | BIGINT | No | — | FK |
| academic_year_id | BIGINT | No | — | FK |
| course_id | BIGINT | No | — | FK |
| section_id | BIGINT | No | — | FK |
| enrollment_date | DATE | No | — | |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(student_id, academic_year_id)`.

---

## 4.13 FacultySubjectAssignment

**Table:** `faculty_subject_assignments`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| faculty_id | BIGINT | No | — | FK |
| subject_id | BIGINT | No | — | FK |
| academic_year_id | BIGINT | No | — | FK |
| is_active | BOOLEAN | No | TRUE | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Unique: `(faculty_id, subject_id, academic_year_id)`.

---

## 4.14 AttendanceSession

**Table:** `attendance_sessions`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| class_id | BIGINT | No | — | FK |
| started_by_id | BIGINT | No | — | FK to User |
| started_at | TIMESTAMPTZ | No | current time | |
| ended_at | TIMESTAMPTZ | Yes | NULL | |
| status | VARCHAR(20) | No | active | CHECK |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Statuses: `active`, `completed`, `cancelled`.

---

## 4.15 Attendance

**Table:** `attendance`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| attendance_session_id | BIGINT | No | — | FK |
| student_id | BIGINT | No | — | FK |
| status | VARCHAR(20) | No | — | CHECK |
| marked_at | TIMESTAMPTZ | No | current time | |
| marked_by_id | BIGINT | Yes | NULL | FK to User |
| correction_reason | TEXT | Yes | NULL | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Statuses: `present`, `absent`, `late`, `excused`.

Unique: `(attendance_session_id, student_id)`.

This enforces the approved no-duplicate-attendance rule.

---

## 4.16 FaceEncoding

**Table:** `face_encodings`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| student_id | BIGINT | No | — | FK, UNIQUE |
| encoding_data | BYTEA | No | — | |
| source_image_path | VARCHAR(500) | Yes | NULL | |
| status | VARCHAR(20) | No | pending | CHECK |
| approved_by_id | BIGINT | Yes | NULL | FK to User |
| approved_at | TIMESTAMPTZ | Yes | NULL | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Statuses: `pending`, `approved`, `rejected`.

Face registration requires administrative approval.

---

## 4.17 Report

**Table:** `reports`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| institution_id | BIGINT | No | — | FK |
| requested_by_id | BIGINT | No | — | FK to User |
| report_type | VARCHAR(50) | No | — | |
| format | VARCHAR(20) | No | — | CHECK |
| status | VARCHAR(20) | No | pending | CHECK |
| file_path | VARCHAR(500) | Yes | NULL | |
| generated_at | TIMESTAMPTZ | Yes | NULL | |
| created_at | TIMESTAMPTZ | No | current time | |
| updated_at | TIMESTAMPTZ | No | current time | |

Formats: `pdf`, `excel`.

Statuses: `pending`, `processing`, `completed`, `failed`.

---

## 4.18 Notification

**Table:** `notifications`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| user_id | BIGINT | No | — | FK |
| title | VARCHAR(200) | No | — | |
| message | TEXT | No | — | |
| notification_type | VARCHAR(50) | No | — | |
| is_read | BOOLEAN | No | FALSE | |
| read_at | TIMESTAMPTZ | Yes | NULL | |
| created_at | TIMESTAMPTZ | No | current time | |

Indexes: `(user_id, is_read)`, `(user_id, created_at)`.

Notification channels are intentionally not specified because the locked requirements do not prescribe them.

---

## 4.19 AuditLog

**Table:** `audit_logs`

| Column | Type | Null | Default | Constraint |
|---|---|---:|---|---|
| id | BIGINT | No | auto | PK |
| actor_user_id | BIGINT | Yes | NULL | FK to User |
| action | VARCHAR(100) | No | — | |
| entity_type | VARCHAR(100) | No | — | |
| entity_id | BIGINT | Yes | NULL | |
| description | TEXT | Yes | NULL | |
| metadata | JSONB | Yes | NULL | |
| ip_address | INET | Yes | NULL | |
| created_at | TIMESTAMPTZ | No | current time | |

Indexes: `actor_user_id`, `(entity_type, entity_id)`, `created_at`, `action`.

Audit records are append-oriented.

---

# 5. Core Relationships

```text
Institution
 ├── Department
 ├── AcademicYear
 ├── Course
 ├── Student
 ├── Report
 └── Configuration / Branding

Department
 └── Faculty

AcademicYear
 ├── Section
 ├── Class
 └── StudentEnrollment

Course
 ├── Subject
 ├── Section
 └── Class

Subject
 ├── FacultySubjectAssignment
 └── Class

Section
 ├── StudentEnrollment
 └── Class

Faculty
 ├── FacultySubjectAssignment
 └── Class

Student
 ├── StudentEnrollment
 ├── FaceEncoding
 └── Attendance

Class
 └── AttendanceSession

AttendanceSession
 └── Attendance
```

---

# 6. Required Integrity Rules

The database must enforce:

1. Primary-key uniqueness.
2. Foreign-key integrity.
3. Institution-scoped department-code uniqueness.
4. Institution-scoped student-roll-number uniqueness.
5. Course-scoped subject-code uniqueness.
6. Academic-year/course section uniqueness.
7. One enrollment per student per academic year.
8. One faculty/subject assignment per academic year.
9. One attendance record per student per attendance session.
10. Valid status values.
11. Valid academic-year dates.
12. One configuration per institution.
13. One branding record per institution.
14. One faculty profile per user.
15. One student profile per user when linked to an account.

Business rules that cannot safely be represented as simple database constraints remain in the service layer.

---

# 7. Index Strategy

The architecture requires indexed important query paths.

Required paths include:

- User email (already unique/indexed).
- Student ID.
- Attendance date/time.
- Class ID.
- Department ID.
- Institution ID.
- `(student_id, marked_at)` for attendance history.
- `(user_id, is_read)` for notifications.
- `(entity_type, entity_id)` for audit lookup.

Duplicate indexes must not be introduced.

---

# 8. Existing Accounts Integration

The existing committed Accounts implementation already owns:

```text
users
roles
```

and uses Django `BigAutoField`.

Those tables remain unchanged.

No duplicate User or Role tables are introduced.

Institution-scoped authorization remains the responsibility of the existing authentication/RBAC and business permission layers, using institutional relationships in the master-data schema.

---

# 9. Implementation Policy

1. Existing Accounts migrations remain unchanged.
2. Existing migration names/order remain unchanged.
3. New tables are introduced through Django migrations.
4. Only tables required by the current roadmap module are implemented at each stage.
5. Defining a future table in this document does not authorize implementing its APIs early.
6. Destructive schema changes require explicit review.
7. Every implemented schema change must pass Django checks and relevant tests.

---

# 10. Phase 3 Mapping

```text
3.1 User Management
    Existing Users / Roles

3.2 Institution Management
    Institution
    InstitutionConfiguration
    InstitutionBranding

3.3 Department Management
    Department

3.4 Academic Structure
    AcademicYear
    Course
    Subject
    Section
    Class

3.5 Faculty
    Faculty
    FacultySubjectAssignment

3.6 Student Management
    Student
    StudentEnrollment
```

Attendance, Face Registration, Reports, Notifications, and Audit Logs are defined physically here for dependency planning, but they are implemented only in their approved future phases.

---

# 11. Design Status

**Status: Approved for implementation in the project workflow.**

This document resolves the physical-schema gap between the locked conceptual architecture and Django implementation.

The original eight planning documents remain authoritative for requirements, scope, architecture, API strategy, security, deployment, and roadmap. This document is the detailed physical database implementation design derived from them.
