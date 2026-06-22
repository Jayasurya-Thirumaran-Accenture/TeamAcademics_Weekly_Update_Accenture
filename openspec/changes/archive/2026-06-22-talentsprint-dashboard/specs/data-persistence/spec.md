## ADDED Requirements

### Requirement: Supabase schema
The system SHALL use three tables in Supabase: `programs`, `sessions`, and `responses`.

`programs` columns: id (uuid, PK), short_name (text, unique), full_name (text), cohort (int), display_order (int), active (bool, default true), created_at (timestamptz).

`sessions` columns: id (uuid, PK), program_id (uuid, FK → programs.id), topic (text), session_date (date), session_time (text), instructor (text), batch_strength (int), zoom_joined (int), total_responses (int), avg_rating (numeric), created_at (timestamptz). Unique constraint on (program_id, session_date, topic).

`responses` columns: id (uuid, PK), session_id (uuid, FK → sessions.id), respondent_name (text), respondent_email (text), rating (int), reason (text), remarks (text).

#### Scenario: Schema created
- **WHEN** the SQL migration is run against a fresh Supabase project
- **THEN** all three tables exist with the specified columns and constraints

### Requirement: Supabase credentials via Streamlit secrets
The system SHALL read the Supabase URL and anon key exclusively from Streamlit secrets (`st.secrets["supabase"]["url"]` and `st.secrets["supabase"]["key"]`). Credentials SHALL NOT be hardcoded or committed to the repository.

#### Scenario: App connects to Supabase
- **WHEN** the app starts with valid secrets configured
- **THEN** the Supabase client initializes and all DB reads succeed

#### Scenario: Missing secrets
- **WHEN** secrets are not configured
- **THEN** the app shows a clear error: "Supabase credentials not configured. See README for setup instructions."

### Requirement: Connection reuse via session state
The Supabase client SHALL be instantiated once per Streamlit session using `st.session_state` to avoid reconnecting on every rerender.

#### Scenario: Client cached in session state
- **WHEN** the app rerenders (e.g., tab switch, file upload)
- **THEN** the existing Supabase client is reused, not recreated

### Requirement: Seed data for initial programs
A SQL seed script SHALL be provided to insert the initial 4 programs: ADSML C9, TS GenAI C2, IIITH GIAPT C1, AIML C27 with display_order 1–4.

#### Scenario: Seed script populates programs
- **WHEN** the seed SQL is run after schema migration
- **THEN** 4 rows exist in the programs table with correct names and order
