# Spec: Program Management

## Purpose

Defines the administrative interface for managing programs in the TalentSprint Dashboard, including adding, editing, deactivating, and reordering programs.

## Requirements

### Requirement: Add new program
The dashboard SHALL provide a form to add a new program with fields: short name (e.g., "ADSML C9"), full name, cohort number, and display order. On submission, the program SHALL be inserted into the programs table and immediately appear as a tab.

#### Scenario: New program added
- **WHEN** a user fills in the add-program form and submits
- **THEN** the program is saved to Supabase and a new tab appears on next page interaction

#### Scenario: Duplicate short name
- **WHEN** a short name is submitted that already exists in the programs table
- **THEN** an error is shown: "A program with this name already exists."

### Requirement: Edit program name
The dashboard SHALL allow editing the short name and full name of an existing program inline. Changes SHALL be saved to Supabase immediately on confirmation.

#### Scenario: Program name edited
- **WHEN** a user edits a program's short name and saves
- **THEN** the tab label updates to the new name on the next render

### Requirement: Deactivate program
The dashboard SHALL allow marking a program as inactive. Inactive programs SHALL not appear as tabs and SHALL not be selectable during Excel upload. Their historical data SHALL be preserved.

#### Scenario: Program deactivated
- **WHEN** a user deactivates a program
- **THEN** its tab disappears from the main view but all session and response records remain in the database

#### Scenario: Reactivate program
- **WHEN** a user reactivates a previously deactivated program
- **THEN** its tab reappears and all historical data is visible again

### Requirement: Reorder programs
The dashboard SHALL allow changing a program's display order via a number input. Programs SHALL be shown in ascending display_order on the tab bar.

#### Scenario: Display order changed
- **WHEN** a user changes a program's display_order value and saves
- **THEN** the tabs reorder to reflect the new position on next render
