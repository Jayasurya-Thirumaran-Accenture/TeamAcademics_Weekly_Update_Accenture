# TalentSprint Dashboard

A Streamlit dashboard for visualizing weekly training program session data across 4 programs. Ops uploads an Excel file → data is stored in Supabase → charts and feedback are shown per program tab.

## One-time Setup

### 1. Supabase

1. Go to [supabase.com](https://supabase.com) → create a new project (free tier)
2. In the Supabase dashboard, open **SQL Editor**
3. Paste and run `sql/schema.sql` to create the tables
4. Paste and run `sql/seed.sql` to add the initial 4 programs
5. Copy your **Project URL** and **anon/public key** from **Project Settings → API**

### 2. GitHub

1. Create a new GitHub repository (public or private)
2. Push this project folder to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

### 3. Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub
2. Click **New app** → select your repository, branch `main`, file `app.py`
3. Click **Advanced settings → Secrets** and paste:
   ```toml
   [supabase]
   url = "https://your-project-id.supabase.co"
   key = "your-anon-key-here"
   ```
4. Click **Deploy** — your app will be live at a `*.streamlit.app` URL

## Weekly Update Workflow

1. Receive Excel file from Ops (Zoom session export)
2. Open your dashboard URL
3. Scroll to the bottom → click **⚙ Admin**
4. Click **Upload Session Data**
5. Drop the `.xlsx` file in the uploader
6. Confirm the auto-detected program (or select manually)
7. Click **Save Session Data**

The dashboard updates immediately — charts and feedback for all programs are visible in the tabs above.

## Running Locally (optional)

```bash
pip install -r requirements.txt
# Create .streamlit/secrets.toml from .streamlit/secrets.toml.example
# Fill in your Supabase URL and key
streamlit run app.py
```

## Adding or Editing Programs

Open **⚙ Admin → Manage Programs** in the dashboard to:
- Add a new program (no code changes needed)
- Edit a program's name
- Deactivate old cohorts (data is preserved)
- Reorder tabs

## Project Structure

```
app.py                      # Main Streamlit app
requirements.txt
sql/
  schema.sql                # Run once in Supabase SQL Editor
  seed.sql                  # Run once to load initial 4 programs
utils/
  db.py                     # Supabase client (cached per session)
  queries.py                # All database read/write functions
  parser.py                 # Excel → structured data
components/
  upload.py                 # Upload UI
  kpi_cards.py              # Avg rating, join rate, response rate
  charts.py                 # Rating trend + attendance trend charts
  feedback.py               # Per-response feedback cards
  session_selector.py       # Session dropdown
  program_manager.py        # Add/edit/deactivate programs
.streamlit/
  secrets.toml.example      # Template — copy to secrets.toml and fill in
```
