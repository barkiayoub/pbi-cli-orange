---
name: Power BI Report
description: >
  Scaffold, validate, preview, and manage Power BI PBIR report projects using
  pbi-cli. Invoke this skill whenever the user mentions "create report", "new
  report", "PBIR", "scaffold", "validate report", "report structure", "preview
  report", "report info", "reload Desktop", "convert report", ".pbip project",
  "report project", or wants to understand the PBIR folder format, set up a new
  report from scratch, or work with the report as a whole. Every report built
  here follows the Orange house style: load that skill first. For
  specific tasks, see also: power-bi-visuals (charts, binding), power-bi-pages
  (page management), power-bi-themes (themes, formatting), power-bi-filters
  (page/visual filters).
tools: pbi-cli
---

# Power BI Report Skill

Manage Power BI PBIR report projects at the top level -- scaffolding, validation,
preview, and Desktop integration. No connection to Power BI Desktop is needed
for most operations.

> **House style is mandatory.** This toolkit only produces dashboards in the
> Orange design system defined in **power-bi-orange-dashboard**: the theme, a
> 1920×1080 `#EFEFEF` page, the kicker/headline/KPI/body/takeaway/footer
> anatomy, and the approved visual types. Load that skill before creating or
> changing any report. Apply the Orange theme right after `report create`.

## PBIR Format

PBIR (Enhanced Report Format) stores reports as a folder of JSON files:

```
MyReport.Report/
  definition.pbir            # dataset reference
  definition/
    version.json             # PBIR version
    report.json              # report settings, theme
    pages/
      pages.json             # page order
      page_abc123/
        page.json            # page settings
        visuals/
          visual_def456/
            visual.json      # visual type, position, bindings
```

Each file has a public JSON schema from Microsoft for validation.
PBIR is GA as of January 2026 and the default format in Desktop since March 2026.

## Creating a Report

```bash
# Scaffold a new report project
pbi report create ./MyProject --name "Sales Report"

# With dataset reference
pbi report create ./MyProject --name "Sales" --dataset-path "../Sales.Dataset"
```

This creates the full folder structure with `definition.pbir`, `report.json`,
`version.json`, and an empty `pages/` directory.

## Report Info and Validation

```bash
# Show report metadata summary (pages, theme, dataset)
pbi report info
pbi report info --path ./MyReport.Report

# Validate report structure and JSON files
pbi report validate
```

Validation checks:
- Every page carries the untouched **Orange Restricted** label (`cls_restricted`,
  `#FF7900`). A missing or altered label is an error. Fix it with
  `pbi report apply-classification`, never by hand.
- Required files exist (`definition.pbir`, `report.json`, `version.json`)
- All JSON files parse without errors
- Schema URLs are present and consistent
- Page references in `pages.json` match actual page folders

## Preview

Start a live HTML preview of the report layout:

```bash
pbi report preview
```

Opens a browser showing all pages with visual placeholders, types, positions,
and data bindings. The preview auto-refreshes when files change.

Requires the `preview` optional dependency: `pip install pbi-cli-tool[preview]`

## Desktop Integration

```bash
# Trigger Power BI Desktop to reload the current report
pbi report reload
```

Power BI Desktop's Developer Mode auto-detects TMDL changes but not PBIR
changes. This command saves and closes the open `.pbip` in Desktop, re-applies
any PBIR edits that Desktop's save would overwrite, then reopens the file.

Requires the `reload` optional dependency (installs `pywin32`):
`pip install pbi-cli-tool[reload]`

## Suppressing Auto-Sync (--no-sync)

By default, every write command (`add-page`, `delete-page`, `set-background`,
`set-theme`, etc.) automatically syncs Power BI Desktop after each operation.
The sync closes Desktop with save and reopens the `.pbip` (it does not send a
keyboard shortcut), so users will see Desktop close and relaunch after each
write. When building a report in multiple steps, this causes Desktop to
close-and-reopen after every single command.

Use `--no-sync` on the `report` command group to suppress per-command syncs,
then call `pbi report reload` once at the end:

```bash
# BAD: Desktop reloads after every command
pbi report add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report set-background synthese --color "#EFEFEF"

# GOOD: suppress sync during build, reload once at the end
pbi report --no-sync add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report --no-sync set-background synthese --color "#EFEFEF"
pbi report reload
```

`--no-sync` is available on: `report`, `visual`, `filters`, and `bookmarks`
command groups.

## Classification Label

```bash
# Add/restore the read-only "Orange Restricted" label on every page (or one page)
pbi report apply-classification
pbi report apply-classification synthese
```

Run it once when taking over a report that pbi-cli did not create. New pages
get the label automatically from `add-page`.

## Convert

```bash
# Convert a .Report folder into a distributable .pbip project
pbi report convert ./MyReport.Report --output ./distributable/
```

## Path Resolution

All report commands auto-detect the `.Report` folder:

1. Explicit: `pbi report --path ./MyReport.Report info`
2. Auto-detect: walks up from CWD looking for `*.Report/definition/`
3. From `.pbip`: finds sibling `.Report` folder from `.pbip` file

## Schema Rules (Don't Break These)

These constraints are not obvious but will silently crash PBI Desktop on open:

### `.pbip` artifacts — only `report` is allowed

The `.pbip` file's `artifacts` array must contain ONLY a `report` entry.
Never add a `dataset` entry — the schema rejects it:

```json
// CORRECT
"artifacts": [{ "report": { "path": "MyReport.Report" } }]

// WRONG — crashes on open with a schema validation error
"artifacts": [
  { "report": { "path": "MyReport.Report" } },
  { "dataset": { "path": "MyModel.SemanticModel" } }
]
```

The semantic model is linked via `definition.pbir`, not the `.pbip` artifacts.

### `definition.pbir` path — must be a non-null string

`datasetReference.byPath.path` must always be a non-null string pointing to the
SemanticModel folder. Setting it to `null` is a schema violation:

```json
// CORRECT
"datasetReference": { "byPath": { "path": "../MyModel.SemanticModel" } }

// WRONG — null is not allowed by the schema
"datasetReference": { "byPath": { "path": null } }
```

### Always validate before opening Desktop

```bash
pbi report validate
```

Run this after every structural change. It catches JSON parse errors (including
trailing commas), missing required files, and broken page references before
PBI Desktop sees them.

## Workflow: Build a Complete Orange Dashboard

This workflow uses commands from multiple skills. Coordinates, visual names,
the theme JSON and the textbox/shape recipes all come from
**power-bi-orange-dashboard**.

```bash
# 1. Scaffold report (this skill)
pbi report create . --name "SalesDashboard" --dataset-path "../SalesModel.SemanticModel"

# 2. Apply the Orange theme immediately (power-bi-orange-dashboard / power-bi-themes)
pbi report --no-sync set-theme --file orange-dashboard-theme.json

# 3. Add 1920x1080 pages on the #EFEFEF canvas (power-bi-pages)
pbi report --no-sync add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report --no-sync set-background synthese --color "#EFEFEF"

# 4. Place the page anatomy on the grid (power-bi-visuals)
pbi visual --no-sync add --page synthese --type textbox --name hdr_kicker   --x 64 --y 40 --width 1792 --height 40
pbi visual --no-sync add --page synthese --type textbox --name hdr_headline --x 64 --y 80 --width 1792 --height 64
pbi visual --no-sync add --page synthese --type card --name kpi_1 --x 64 --y 168 --width 430 --height 152
pbi visual --no-sync add --page synthese --type bar  --name viz_1 --x 64 --y 344 --width 884 --height 572
# ... remaining tiles, body visuals, takeaway bar and footer per the grid

# 5. Bind data (power-bi-visuals)
pbi visual --no-sync bind kpi_1 --page synthese --field "Sales[Total Revenue]"
pbi visual --no-sync bind viz_1 --page synthese --category "Geo[Region]" --value "Sales[Amount]"

# 6. Write the textbox/shape recipes into the decorative visual.json files

# 7. Validate (this skill) and reload Desktop once
pbi report validate
pbi report reload
```

Never finish a report without the theme, the full page anatomy and a passing
`pbi report validate`.

## Combining Model and Report

pbi-cli covers both the semantic model layer and the report layer:

```bash
# Model layer (requires pbi connect)
pbi connect
pbi measure create "Total Revenue" -e "SUM(Sales[Amount])" -t Sales

# Report layer (no connection needed)
pbi report create . --name "Sales"
pbi visual add --page synthese --type card --name kpi_1 --x 64 --y 168 --width 430 --height 152
pbi visual bind kpi_1 --page synthese --field "Sales[Total Revenue]"
```

## Related Skills

| Skill | When to use |
|-------|-------------|
| **power-bi-orange-dashboard** | Design system: theme, grid, anatomy, recipes (always) |
| **power-bi-visuals** | Add, bind, update, delete visuals |
| **power-bi-pages** | Add, remove, configure pages and bookmarks |
| **power-bi-themes** | Themes, conditional formatting |
| **power-bi-filters** | Page and visual filters |

## JSON Output

```bash
pbi --json report info
pbi --json report validate
```
