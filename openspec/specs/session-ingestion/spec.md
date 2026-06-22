# Spec: Session Ingestion

## Purpose

Defines the process for uploading Zoom session Excel exports into the TalentSprint Dashboard, including file parsing, program auto-detection, metadata extraction, and response ingestion.

## Requirements

### Requirement: Excel file upload
The dashboard SHALL provide a file uploader that accepts `.xlsx` files. On upload, the system SHALL parse the file, extract metadata and responses, and persist them to Supabase.

#### Scenario: Valid file uploaded
- **WHEN** a user uploads a valid Zoom session Excel file
- **THEN** the system parses it, shows a preview summary (program name, date, response count), and asks for confirmation before saving

#### Scenario: Duplicate session uploaded
- **WHEN** a file with the same program + session date already exists in the database
- **THEN** the system warns "Session already exists for [Program] on [Date]. Overwrite?" with confirm/cancel buttons

#### Scenario: Invalid file format
- **WHEN** a file is uploaded that does not match the expected schema (missing Program Name in row 1, or no response table)
- **THEN** the system shows an error: "File format not recognized. Expected Zoom session export format."

### Requirement: Auto-detect program from file
The system SHALL read the Program Name value from row 1, column B of the Excel file and fuzzy-match it against active programs in the database to identify the target program.

#### Scenario: High-confidence match
- **WHEN** the Excel Program Name contains keywords matching exactly one active program
- **THEN** the matched program is pre-selected and shown to the user for confirmation

#### Scenario: Low-confidence or ambiguous match
- **WHEN** the Excel Program Name does not clearly match any active program
- **THEN** a dropdown of all active programs is shown and the user must select manually before saving

### Requirement: Parse session metadata
The system SHALL extract the following fields from the Excel header rows (1–11): Program Name, Cohort, Instructor, Topic, Session Date, Session Time, Total Batch Strength, Zoom Joined, Total Responses. Average rating SHALL be computed from the response data, not taken from the formula cell.

#### Scenario: All metadata fields extracted
- **WHEN** a valid Excel file is parsed
- **THEN** all metadata fields are populated; missing optional fields (e.g., Session Time) are stored as NULL

### Requirement: Parse individual responses
The system SHALL extract all response rows starting from row 14, reading: Name, Email, Rating (integer 1–10), Reason (text), Remarks (text). Rows where all fields are NULL SHALL be skipped.

#### Scenario: Responses extracted
- **WHEN** the Excel file has 2 response rows
- **THEN** exactly 2 response records are inserted into the responses table linked to the session

#### Scenario: Empty rows skipped
- **WHEN** the file contains blank rows between responses
- **THEN** blank rows are ignored and only rows with at least a Name or Rating are saved
