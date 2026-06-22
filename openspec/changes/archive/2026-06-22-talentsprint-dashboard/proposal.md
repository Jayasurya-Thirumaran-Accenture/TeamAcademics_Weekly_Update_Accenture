## Why

The team currently tracks training program feedback by manually extracting data from Zoom session Excel exports and writing RST files in GitLab — a process that produces plain text with no visualizations, no trend tracking, and no easy way to compare sessions over time. A visual dashboard will make weekly manager presentations faster to prepare and more informative.

## What Changes

- New web-based dashboard hosted at a persistent URL (Streamlit Community Cloud)
- Automated Excel ingestion: drag-and-drop upload parses Zoom session exports, auto-detects the program, and stores data in a persistent database
- Per-program pages (4 programs, editable list) showing KPI cards, rating trends, attendance trends, and feedback comments
- Admin section for uploading new session data and managing the program list
- Supabase (PostgreSQL) as the persistent data store
- GitHub repository hosts the application code, connected to Streamlit Community Cloud for continuous deployment

## Capabilities

### New Capabilities

- `program-dashboard`: Per-program view with KPI cards (avg rating, participation %, response count), rating trend chart, attendance trend chart, and paginated feedback comments per session
- `session-ingestion`: Excel upload UI that parses Zoom session export format (metadata in rows 1-11, response table from row 13), auto-detects the program from the file's Program Name field, and persists sessions + individual responses to Supabase
- `program-management`: Admin UI to add, edit, reorder, and deactivate programs without code changes
- `data-persistence`: Supabase schema (programs, sessions, responses tables) with connection management via Streamlit secrets

### Modified Capabilities

<!-- None — this is a greenfield project -->

## Impact

- New dependencies: `streamlit`, `supabase-py`, `openpyxl`, `pandas`, `plotly`
- External services: Supabase (free tier), Streamlit Community Cloud (free), GitHub
- No impact on existing GitLab RST workflow until team is ready to migrate
- Supabase free tier limits: 500MB storage, 2 projects — well within scope for this use case
