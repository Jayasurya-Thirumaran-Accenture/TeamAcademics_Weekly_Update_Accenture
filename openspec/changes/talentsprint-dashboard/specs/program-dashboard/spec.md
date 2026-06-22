## ADDED Requirements

### Requirement: Program tab navigation
The dashboard SHALL display one tab per active program, ordered by display_order from the programs table. Switching tabs SHALL show that program's data without a full page reload.

#### Scenario: Tabs render from DB
- **WHEN** the app loads
- **THEN** one tab per active program is shown, labeled with the program's short name (e.g., "ADSML C9")

#### Scenario: No active programs
- **WHEN** the programs table has no active records
- **THEN** the app displays a message: "No programs configured. Add one in the Manage Programs section."

### Requirement: KPI cards for latest session
Each program tab SHALL display three metric cards at the top showing stats from the most recent session: average rating (out of 10), Zoom join rate (Zoom Joined / Batch Strength as %), and response rate (Responses / Zoom Joined as %).

#### Scenario: Latest session KPIs displayed
- **WHEN** a program tab is selected and at least one session exists
- **THEN** three cards show: avg rating formatted as "X.X / 10", join rate as "XX%", response rate as "XX%"

#### Scenario: No sessions yet
- **WHEN** a program has no sessions uploaded
- **THEN** KPI cards show "—" and a message: "No session data yet. Upload the first session below."

### Requirement: Rating trend chart
The dashboard SHALL display a line chart of average rating per session over time for the selected program, with session date on the x-axis and rating (0–10) on the y-axis.

#### Scenario: Multiple sessions charted
- **WHEN** a program has two or more sessions
- **THEN** a Plotly line chart renders with one data point per session, ordered chronologically

#### Scenario: Single session
- **WHEN** a program has exactly one session
- **THEN** a single-point line chart is shown (not hidden)

### Requirement: Attendance trend chart
The dashboard SHALL display a grouped bar chart showing Batch Strength, Zoom Joined, and Total Responses per session over time.

#### Scenario: Attendance bars rendered
- **WHEN** a program has at least one session
- **THEN** a Plotly grouped bar chart shows three bars per session date

### Requirement: Session feedback display
The dashboard SHALL display all individual responses for the most recently selected session, showing the respondent's name, rating, reason/comment, and remarks (if present) as styled cards.

#### Scenario: Feedback cards shown
- **WHEN** a session is selected (defaults to most recent)
- **THEN** each response row renders as a card with rating badge, name, comment text, and remarks

#### Scenario: Session selector
- **WHEN** a program has multiple sessions
- **THEN** a dropdown allows selecting any past session to view its feedback
