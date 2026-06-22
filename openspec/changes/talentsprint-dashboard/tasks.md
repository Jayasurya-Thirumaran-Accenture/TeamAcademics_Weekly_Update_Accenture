## 1. Project Setup

- [ ] 1.1 Create GitHub repository and push initial project structure (`app.py`, `requirements.txt`, `.gitignore`, `README.md`)
- [x] 1.2 Add dependencies to `requirements.txt`: `streamlit`, `supabase`, `openpyxl`, `pandas`, `plotly`
- [ ] 1.3 Create Supabase project and note the project URL and anon key
- [ ] 1.4 Run schema migration SQL in Supabase SQL editor (create `programs`, `sessions`, `responses` tables with constraints)
- [ ] 1.5 Run seed SQL to insert initial 4 programs (ADSML C9, TS GenAI C2, IIITH GIAPT C1, AIML C27)
- [ ] 1.6 Connect GitHub repo to Streamlit Community Cloud and configure Supabase credentials in Streamlit secrets

## 2. Data Layer

- [x] 2.1 Create `utils/db.py`: Supabase client factory using `st.session_state` caching; raise clear error if secrets missing
- [x] 2.2 Create `utils/queries.py`: functions for `get_active_programs()`, `get_sessions(program_id)`, `get_responses(session_id)`, `upsert_session()`, `insert_responses()`
- [x] 2.3 Create `sql/schema.sql`: full schema DDL for `programs`, `sessions`, `responses` tables (for documentation and reuse)
- [x] 2.4 Create `sql/seed.sql`: INSERT statements for the 4 initial programs

## 3. Excel Parser

- [x] 3.1 Create `utils/parser.py`: function `parse_session_excel(file_bytes)` that extracts metadata from rows 1–11 and response rows from row 14 onward
- [x] 3.2 Implement program auto-detection: extract Program Name from row 1 col B, normalize and fuzzy-match against active programs list
- [x] 3.3 Handle edge cases: blank response rows (skip), missing optional fields (store NULL), formula cells in avg_rating (compute from response data instead)
- [x] 3.4 Return structured dict: `{ metadata: {...}, responses: [...], matched_program_id: uuid | None, match_confidence: float }`

## 4. Session Upload UI

- [x] 4.1 Create `components/upload.py`: `render_upload_section()` using `st.file_uploader` for `.xlsx` files
- [x] 4.2 Show parsed preview on upload: program name, session date, topic, response count — before saving
- [x] 4.3 If match confidence is low, show program selection dropdown for manual override
- [x] 4.4 Handle duplicate session: query for existing (program_id, session_date, topic); show overwrite warning with confirm/cancel
- [x] 4.5 On confirmation, call `upsert_session()` then `insert_responses()`, show success message with session summary

## 5. Program Dashboard View

- [x] 5.1 Create `components/kpi_cards.py`: `render_kpi_cards(session)` displaying avg rating, join rate, response rate as `st.metric` cards in a 3-column layout
- [x] 5.2 Create `components/charts.py`: `render_rating_trend(sessions_df)` Plotly line chart, `render_attendance_trend(sessions_df)` Plotly grouped bar chart
- [x] 5.3 Create `components/feedback.py`: `render_feedback_cards(responses_df)` displaying each response as a styled card with rating badge, name, comment, and remarks
- [x] 5.4 Create `components/session_selector.py`: dropdown that lists all sessions for a program ordered by date descending; defaults to most recent

## 6. Main App & Tab Navigation

- [x] 6.1 In `app.py`, load active programs from DB on startup; render `st.tabs()` from the program list
- [x] 6.2 For each tab: fetch sessions for that program, render KPI cards (latest session), rating trend chart, attendance trend chart, session selector, and feedback cards
- [x] 6.3 Handle empty-program state: show placeholder message when no sessions exist
- [x] 6.4 Add collapsible "Admin" expander at bottom of page containing the upload section and program management section

## 7. Program Management UI

- [x] 7.1 Create `components/program_manager.py`: `render_program_manager()` showing table of current programs with edit/deactivate controls
- [x] 7.2 Implement add-program form: short name, full name, cohort, display order fields; validate for duplicate short name before insert
- [x] 7.3 Implement inline edit for short name and full name; save to Supabase on confirmation
- [x] 7.4 Implement deactivate/reactivate toggle per program; confirm before deactivating
- [x] 7.5 Implement display order number input; save and reorder tabs on next render

## 8. Polish & Deployment

- [x] 8.1 Add page config: `st.set_page_config(page_title="TalentSprint Dashboard", layout="wide")`
- [x] 8.2 Write `README.md` with setup instructions: Supabase schema setup, secrets configuration, local run, and Streamlit Cloud deploy steps
- [ ] 8.3 Test full upload flow end-to-end with the sample ADSML Cohort 8 Excel file
- [ ] 8.4 Verify all 4 program tabs render correctly after seed data is loaded
- [ ] 8.5 Confirm app is accessible at the Streamlit Community Cloud URL
