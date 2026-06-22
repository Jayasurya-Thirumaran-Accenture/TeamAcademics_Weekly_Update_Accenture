## Context

The team runs 4 training programs (ADSML C9, TS GenAI C2, IIITH GIAPT C1, AIML C27) and receives session feedback as Zoom-generated Excel exports after each session. Currently, data is manually transcribed into RST files on GitLab and presented to a manager in weekly meetings. The new system must be free, require no server management, and be updatable by a non-developer (drag-and-drop Excel upload).

Excel format (consistent, from Zoom):
- Rows 1–11: key-value metadata (Program Name, Cohort, Instructor, Topic, Date, Batch Strength, Zoom Joined, Responses, Avg Rating)
- Row 13: column headers
- Rows 14+: individual responses (Name, Email, Rating 1–10, Reason, Remarks)

## Goals / Non-Goals

**Goals:**
- Persistent, hosted dashboard accessible via URL
- Upload-based data ingestion (no CLI required for weekly updates)
- Per-program tab view with rating/attendance trend charts and feedback display
- Editable program list (no code changes to add/rename programs)
- Fully free infrastructure

**Non-Goals:**
- Real-time data sync or Zoom API integration
- User authentication / role-based access (internal team use only)
- Mobile-optimized layout
- Exporting dashboard as PDF or image
- Historical data migration from existing RST files

## Decisions

### 1. Streamlit over React/Next.js

**Decision:** Use Streamlit for the application framework.

**Rationale:** The entire team is Python-familiar (data science context). Streamlit produces interactive dashboards with minimal code — charts, file uploaders, and tab navigation are built-in. A React app would require JavaScript expertise and a separate API layer for the same outcome.

**Alternative considered:** Next.js + Vercel — rejected due to higher build complexity and no clear advantage for an internal tool with one update author.

### 2. Supabase over GitHub repo as data store

**Decision:** Use Supabase (PostgreSQL) for all persistent data.

**Rationale:** Streamlit Community Cloud has no persistent filesystem between deployments. Storing data as committed JSON files in GitHub would require a GitHub token in the app and a git commit per upload — fragile and slow. Supabase provides a proper relational store, free at this scale, with a Python client that works cleanly from Streamlit.

**Alternative considered:** GitHub repo JSON files — rejected due to the commit-per-upload workflow complexity and lack of queryability.

### 3. Auto-detect program from Excel metadata, not filename

**Decision:** Parse row 1 of the Excel (`Program Name` field) to identify the program, then fuzzy-match against the programs table.

**Rationale:** Filenames are consistent but contain cohort numbers that will change (Cohort 8 → Cohort 9). The Program Name cell contains the canonical full name which is more stable and unambiguous.

**Matching logic:** Normalize both strings (lowercase, strip punctuation), check for keyword overlap. If match confidence is below threshold, show a dropdown for the user to confirm/select manually.

### 4. Streamlit multipage app with tab-per-program UI

**Decision:** Single Streamlit app with `st.tabs()` for program switching, not Streamlit multipage (separate `.py` files per page).

**Rationale:** Programs are dynamic (stored in DB, editable). Streamlit multipage requires static file-per-page. Using `st.tabs()` with a list from the DB means adding a program requires no file changes — just a DB row.

### 5. Plotly for charts

**Decision:** Use Plotly (via `plotly.express`) for all charts.

**Rationale:** Plotly integrates natively with Streamlit (`st.plotly_chart`), supports interactive hover/zoom, and handles time-series line charts and bar charts cleanly. Altair is an alternative but has a steeper learning curve for this team.

## Risks / Trade-offs

**Supabase free tier limits** → 500MB storage, pauses after 1 week of inactivity. At ~50 responses/session × 52 sessions/year × 4 programs, storage stays well under 10MB. Inactivity pause is mitigated by weekly usage pattern.

**Streamlit Community Cloud cold starts** → App sleeps after ~7 days of inactivity, takes 30–60s to wake. Since the dashboard is used weekly, the first weekly open may be slow. Mitigation: open the URL a few minutes before the manager meeting.

**No authentication** → Anyone with the URL can view and upload data. Acceptable for internal team use; if this becomes a concern, Streamlit Community Cloud supports Google OAuth viewer restrictions.

**Program name matching reliability** → Fuzzy matching may fail if program names change significantly. Mitigation: the manual confirmation dropdown is always available as fallback.

## Migration Plan

1. Set up Supabase project and run schema migration SQL
2. Create GitHub repo, push Streamlit app code
3. Connect GitHub repo to Streamlit Community Cloud
4. Add Supabase credentials to Streamlit secrets
5. Upload historical session data manually via the upload UI (optional)
6. Share URL with team — RST workflow can continue in parallel until team is comfortable

No rollback needed — this is additive. Existing GitLab RST files are unaffected.

## Open Questions

- Should the upload section be always visible or hidden behind a toggle/password? (Current plan: visible but clearly labeled as admin section)
- Do all 4 programs follow the same Excel schema, or do some have additional/different columns?
