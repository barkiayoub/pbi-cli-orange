---
name: Power BI Pages
description: >
  Manage Power BI report pages and bookmarks -- add, remove, configure, and lay
  out pages in PBIR reports using pbi-cli. Invoke this skill whenever the user
  mentions "add page", "new page", "delete page", "page layout", "page size",
  "page background", "hide page", "show page", "drillthrough", "page order",
  "page visibility", "page settings", "page navigation", "bookmark", "create
  bookmark", "save bookmark", "delete bookmark", or wants to manage bookmarks
  that capture page-level state. Also invoke when the user asks about drillthrough
  configuration or pageBinding. Pages follow the Orange house style.
tools: pbi-cli
---

# Power BI Pages Skill

Manage pages in PBIR reports. Pages are folders inside `definition/pages/`
containing a `page.json` file and a `visuals/` directory. No Power BI Desktop
connection is needed.

## Orange Page Standard (mandatory)

Every page of an Orange dashboard:
- is **1920×1080**: always pass `--width 1920 --height 1080`, because the CLI default
  of 1280×720 does not match the Orange grid;
- has the **`#EFEFEF` canvas**: run `pbi report set-background <page> --color "#EFEFEF"`
  (the Orange theme also sets it; set it explicitly anyway);
- carries the full anatomy from **power-bi-orange-dashboard**: kicker, conclusion
  headline, KPI row, body visuals, black takeaway bar, footer and two-digit orange
  page number;
- carries the **Orange Restricted** label (`cls_restricted`, `#FF7900`). `add-page`
  inserts it automatically. It is read-only: never edit or remove it. On pages
  created outside pbi-cli, run `pbi report apply-classification`. Hidden
  drillthrough and tooltip pages carry it too;
- has a **short display name** in the dashboard's language ("Synthèse",
  "Détail régional", "Recommandations"). Order the pages as synthesis → detail → recommendations;
  page numbers start at `01`.

Drillthrough and tooltip pages are hidden. They still use the canvas colour and
fonts, but they do not need the takeaway bar.

## Listing and Inspecting Pages

```bash
# List all pages with display names, order, and visibility
pbi report list-pages

# Get full details of a specific page
pbi report get-page page_abc123
```

`get-page` returns:
- `name`, `display_name`, `ordinal` (sort order)
- `width`, `height` (canvas size in pixels)
- `display_option` (e.g. `"FitToPage"`)
- `visual_count` -- how many visuals on the page
- `is_hidden` -- whether the page is hidden in the navigation pane
- `page_type` -- `"Default"` or `"Drillthrough"`
- `filter_config` -- page-level filter configuration (if any)
- `visual_interactions` -- custom visual interaction rules (if any)
- `page_binding` -- drillthrough parameter definition (if drillthrough page)

## Adding Pages

```bash
# Orange standard: explicit folder name, 1920x1080, then the canvas colour
pbi report add-page --display-name "Synthèse" --name synthese \
    --width 1920 --height 1080
pbi report set-background synthese --color "#EFEFEF"
```

The CLI default canvas is 1280×720. Orange dashboards always use 1920×1080,
because every grid coordinate in power-bi-orange-dashboard assumes that size.

## Deleting Pages

```bash
# Delete a page and all its visuals
pbi report delete-page page_abc123
```

This removes the entire page folder including all visual subdirectories.

## Page Background

```bash
# Orange canvas -- the only page background used
pbi report set-background synthese --color "#EFEFEF"
```

## Page Visibility

Control whether a page appears in the report navigation pane:

```bash
# Hide a page (useful for drillthrough or tooltip pages)
pbi report set-visibility page_abc123 --hidden

# Show a hidden page
pbi report set-visibility page_abc123 --visible
```

## Bookmarks

Bookmarks capture page-level state (filters, visibility, scroll position).
They live in `definition/bookmarks/`:

```bash
# List all bookmarks in the report
pbi bookmarks list

# Get details of a specific bookmark
pbi bookmarks get "My Bookmark"

# Add a new bookmark
pbi bookmarks add "Executive View"

# Delete a bookmark
pbi bookmarks delete "Old Bookmark"

# Toggle bookmark visibility
pbi bookmarks set-visibility "Draft View" --hidden
```

## Drillthrough Pages

Drillthrough pages have a `pageBinding` field in `page.json` that defines the
drillthrough parameter. When you call `get-page` on a drillthrough page, the
`page_binding` field returns the full binding definition including parameter
name, bound filter, and field expression. Regular pages return `null`.

To create a drillthrough page, add a page and then configure it as drillthrough
in Power BI Desktop (PBIR drillthrough configuration is not yet supported via
CLI -- the CLI can read and report on drillthrough configuration).

## Workflow: Set Up Report Pages

```bash
# 1. Add pages in order: synthesis -> detail -> recommendations (all 1920x1080)
pbi report --no-sync add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report --no-sync add-page --display-name "Détail régional" --name detail --width 1920 --height 1080
pbi report --no-sync add-page --display-name "Recommandations" --name reco --width 1920 --height 1080
pbi report --no-sync add-page --display-name "Drill région" --name region_drill --width 1920 --height 1080

# 2. Hide the drillthrough page from navigation
pbi report --no-sync set-visibility region_drill --hidden

# 3. Orange canvas on every page
for p in synthese detail reco region_drill; do
  pbi report --no-sync set-background $p --color "#EFEFEF"
done

# 4. Verify the setup (every page 1920x1080), then reload once
pbi --json report list-pages
pbi report reload
```

## Path Resolution

Page commands inherit the report path from the parent `pbi report` group:

1. Explicit: `pbi report --path ./MyReport.Report list-pages`
2. Auto-detect: walks up from CWD looking for `*.Report/definition/`
3. From `.pbip`: finds sibling `.Report` folder from `.pbip` file

## Suppressing Auto-Sync (--no-sync)

By default, every write command automatically syncs Power BI Desktop. When
setting up multiple pages in sequence, Desktop reloads after each one.

Use `--no-sync` on the `report` command group to batch all page changes, then
call `pbi report reload` once at the end:

```bash
# Suppress sync while setting up pages
pbi report --no-sync add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report --no-sync add-page --display-name "Détail" --name detail --width 1920 --height 1080
pbi report --no-sync set-background synthese --color "#EFEFEF"
pbi report --no-sync set-background detail --color "#EFEFEF"

# Single reload when all page setup is done
pbi report reload
```

## JSON Output

```bash
pbi --json report list-pages
pbi --json report get-page page_abc123
pbi --json bookmarks list
```
