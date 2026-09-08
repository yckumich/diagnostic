# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

----------------------Preferred work style---------------------------------
## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.
-------------------------------------------------------

## Running the App

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run 🏠_Home.py
```

App runs at `http://localhost:8501`.

**Gotcha:** `.streamlit/config.toml` pins `[browser] serverAddress` to the production host, so
`streamlit run` prints and opens the *deployed* URL, not the local one. Browse to
`http://localhost:8501` directly, or override:
`--browser.serverAddress=localhost --browser.serverPort=8501`.

## Architecture Overview

This is a multi-page Streamlit app for exploring an Essential Diagnostics List (EDL) for Universal Health Coverage research. **There is no backend database** — all data is read from a single CSV at `static/tableau3_t2_tjfs_join_edl_dashadmin.csv`.

The site presents two tools: the **Essential Diagnostics Explorer** (page 1) and the
**Diagnostic Network Planner** (pages 2–4, presented to users as Steps 1–3).

### Data Layer (`data/database.py`)

`get_view_df()` is the single entry point for all data. It reads the master CSV and applies any active custom tier filters by doing **inner joins** against DataFrames stored in `st.session_state`:
- `custom_condition_df` (keyed on `conditionname` + `conditionlevel`)
- `custom_test_tier_df` (keyed on `test_format`)

When these session state values are `None` or empty, `get_view_df()` returns the full dataset unfiltered.

### Filter Pipeline (Page 1)

`utils/dataframe_utils/filter.py` defines `high_level_filter_map`: a nested dict mapping UI label → CSV column name. This powers the sidebar multiselects on Page 1.

The chain: `high_level_filter_map` → `get_filter()` builds unique-value lists → sidebar renders multiselects → `convert_selection_to_df()` converts selections to a pandas query string → `get_view_df().query(...)`.

### Tab Content System (Page 1)

`utils/dataframe_utils/center_tabs.py::centner_tab_dict` maps tab titles to sub-DataFrame titles. In `utils_center_tab.py`, function names are **derived dynamically** from tab/sub-titles:

```python
f"get_{tab_title}_{df_title}".replace(" ", "_").lower()
# e.g. "get_diagnostic_details_diagnostic_by_domain"
```

When adding a new tab or column, add an entry to `centner_tab_dict` and define a matching function in `utils_center_tab.py`.

### Session State Keys

These are initialized in `🏠_Home.py` and expected across all pages:
- `custom_condition_list` / `custom_condition_df` — built on Page 2
- `custom_test_tier_list` / `custom_test_tier_df` — built on Page 3
- `show_plot`, `show_test_tier_plot` — plot visibility toggles
- `selected_test_names` — test name filter from AgGrid row selection on Page 1

Both `custom_*_list` and `custom_*_df` must be set together; clearing the list must also null the DataFrame (enforced at the top of Page 1).

### Pages

| File | Purpose |
|---|---|
| `🏠_Home.py` | Landing page; initializes all session state keys |
| `pages/1_🗂️_Explore_Diseases_Medicines_and_Diagnostics.py` | Essential Diagnostics Explorer: sidebar filters + tabbed DataFrames + AgGrid test-name selector |
| `pages/2_🩺_Step_1_-_Set_Condition_Tiers.py` | Build/upload the Condition Tiers table |
| `pages/3_🧪_Step_2_-_Set_Diagnostic-Format_Tiers.py` | Build/upload the Diagnostic-Format Tiers table |
| `pages/4_📍_Step_3_-_Diagnostic_Network_Planner_Results.py` | Generate and export the placement summary (PDF via reportlab) |
| `pages/5_📖_Background.py` | Project background, evidence base, linked publications |
| `pages/6_ℹ️_About.py` | Funders, acknowledgements, disclaimer, contact |

Streamlit derives the sidebar label **and the public URL** from the filename — renaming a page
changes its URL.

### Sidebar section headings

`style.py::get_sidebar_style()` injects CSS that renders three group headings in the page nav
("Essential Diagnostics Explorer", "Diagnostic Network Planner", "Project Information"). Streamlit's
file-based navigation has no hook for these, so each heading is a `::before` on the `<li>` that starts
its group, matched by **page URL** rather than `nth-child` so inserting a page cannot shift a heading
onto the wrong item. It depends on Streamlit 1.39.0's DOM (`ul[data-testid="stSidebarNavItems"] > li >
div > a`) — re-check if that pin moves. It must be called on **every** page.

### Sidebar instruction text

The instructions shown in each tool page's sidebar are **hardcoded in Python**, not in markdown:

| Page | Location |
|---|---|
| Explorer | `utils/dataframe_utils/utils.py` → `sidebar_instruction` |
| Step 1 | `utils/condition_tier_utils/utils.py` → `add_sidebar()` |
| Step 2 | `utils/test_tier_utils/utils.py` → `add_sidebar()` |
| Step 3 | `utils/tests_summary_utils/utils.py` → `add_sidebar()` |

### Static Assets

```
static/tableau3_t2_tjfs_join_edl_dashadmin.csv  ← master dataset (single source of truth)
static/lancet_condition_level.csv               ← Lancet reference condition tiers
static/lancet_test_tier.csv                     ← Lancet reference test-format tiers
supplements/                                    ← reference PDFs/CSVs; no longer served by any page
```

Home previously offered `supplements/original_research.pdf` and `supplements/WHO_report.pdf` as download
buttons. Those were removed — Background links to the publications instead. The files remain on disk but
nothing references them.

## Naming Conventions

User-facing vocabulary is **"Condition Tiers"** and **"Diagnostic-Format Tiers"**. The older names
("Diagnostic Test Dashboard", "Diagnostic Placement Tool", "Custom … Tier") are gone from all
user-visible strings.

**Do not rename these**, despite how they read — they are DataFrame column keys, not labels:

- `'Custom Condition Tier'` and `'Test Format Custom Tier'` in `utils/tests_summary_utils/utils.py`
  (`rename_map`, then used for filtering throughout `generate_tests_summary`). They are dropped before
  display — the exported columns are `service / tier / test_format / test_name` — so renaming them
  breaks summary generation while changing nothing a user sees.
- Session-state keys (`custom_condition_df`, `custom_test_tier_list`, …) and CSV column names
  (`custom_condition_tier`, `custom_test_tier`, `test_format`). The CSV names also appear in
  user-facing upload instructions and must stay accurate to the data.

## Line Endings

Four tracked files use **CRLF** while the rest of the repo uses LF: `README.md`,
`utils/condition_tier_utils/utils.py`, `utils/test_tier_utils/utils.py`,
`utils/tests_summary_utils/utils.py`.

Python's text-mode read/write silently converts CRLF → LF, turning a small edit into a whole-file diff.
Open these in binary mode, and check `git diff --stat` before trusting a diff.

## Production Deployment

Docker Compose on `lee-edl.miserver.it.umich.edu` (Ubuntu, `141.211.145.96`). nginx reverse proxy forwards port 80 → Streamlit on port 8501.

Deploy workflow: push to GitHub → SSH to server → `sudo docker build --no-cache -t diagnostic:0.0.X .` → update tag in `docker-compose.yml` → `sudo docker compose down && sudo docker compose up -d`.

Always bump the image tag on each build. The Dockerfile clones from GitHub, so the build picks up whatever is on `main`.
