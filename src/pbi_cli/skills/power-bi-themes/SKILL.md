---
name: Power BI Themes
description: >
  Apply, inspect, and compare Power BI report themes and conditional formatting
  rules using pbi-cli. Invoke this skill whenever the user mentions "theme",
  "colours", "colors", "branding", "dark mode", "corporate theme", "styling",
  "conditional formatting", "colour scale", "gradient", "data bars",
  "background colour", "formatting rules", "visual formatting", or wants to
  change the overall look-and-feel of a report or apply data-driven formatting
  to specific visuals. The only theme used is the Orange house theme.
tools: pbi-cli
---

# Power BI Themes Skill

Manage report-wide themes and per-visual conditional formatting. No Power BI
Desktop connection is needed.

## Orange Theme Lock (mandatory)

Every report uses one theme: **"Orange Dashboard"**. Its full JSON is in
**power-bi-orange-dashboard**. Copy it exactly to `orange-dashboard-theme.json`
and apply it right after `pbi report create`. Do not write, download or apply
any other theme, and do not edit its colours. If the user asks for other
colours or a dark mode, explain that the toolkit is locked to the Orange style
and ask before deviating.

Brand palette (the only colours allowed anywhere):

| Token | Hex | Role |
|---|---|---|
| Accent | `#FF7900` | Primary measure (AC), accent bars, insight stripe; as text only on black (page number, label) |
| Ink | `#111111` | Titles, KPI values, PL/target lines, footer band |
| Body | `#555555` | Labels, axes, PY series |
| Canvas | `#EFEFEF` | Page background, grid lines, neutral cells |
| Card | `#FFFFFF` | Visual tiles |
| Accent tint | `#FFF1E5` | Highlighted target cells |
| Stage colours | `#9A9A9A` `#A8683A` `#D9A400` | Extra series / staged processes only |

Font: Arial everywhere.

## Applying a Theme

Power BI themes are JSON files that define colours, fonts, and visual defaults
for the entire report. Apply the Orange theme with:

```bash
pbi report set-theme --file orange-dashboard-theme.json
```

This copies the theme file into the report's `StaticResources/RegisteredResources/`
folder and updates `report.json` to reference it. The theme takes effect when
the report is opened in Power BI Desktop.

## Inspecting the Current Theme

```bash
pbi report get-theme
```

Returns:
- `base_theme` -- the built-in theme name (e.g. `"CY24SU06"`)
- `custom_theme` -- custom theme name if one is applied (or `null`)
- `theme_data` -- full JSON of the custom theme file (if it exists)

## Comparing Themes

Before applying a new theme, preview what would change:

```bash
pbi report diff-theme --file proposed-theme.json
```

Returns:
- `current` / `proposed` -- display names
- `added` -- keys in proposed but not current
- `removed` -- keys in current but not proposed
- `changed` -- keys present in both but with different values

This helps catch unintended colour changes before committing.

## Theme JSON Structure

The Orange theme's top-level keys (full file in power-bi-orange-dashboard):

```json
{
  "name": "Orange Dashboard",
  "dataColors": ["#FF7900", "#555555", "#111111", "#9A9A9A", "#A8683A", "#D9A400"],
  "background": "#FFFFFF",
  "foreground": "#111111",
  "tableAccent": "#FF7900",
  "textClasses": { ... Arial, 12-36 pt ... },
  "visualStyles": { ... white tiles, no borders/shadows/headers, #EFEFEF page ... }
}
```

Key sections:
- `dataColors` -- palette for data series (6-12 colours recommended)
- `background` / `foreground` -- page and text defaults
- `tableAccent` -- header colour for tables and matrices
- `visualStyles` -- per-visual-type overrides (font sizes, padding, etc.)

See [Microsoft theme documentation](https://learn.microsoft.com/power-bi/create-reports/desktop-report-themes) for the full schema.

## Invalid Properties to Avoid

These properties look plausible but are **not in PBI's theme schema**. Including
them causes PBI Desktop to fail silently or crash when loading the report:

| Property | Location | Why invalid |
|---|---|---|
| `"radius": 8` | Inside `border` objects in `visualStyles` | Borders only accept `color` and `show` |
| `"page": { ... }` | Top-level key | Legacy pbiviz format — not valid in report themes |
| `"dropShadow": { "position": "Inner" }` | Inside `visualStyles` | No `position` sub-property exists for dropShadow |

**Safe top-level keys** for a custom theme:
`name`, `dataColors`, `background`, `foreground`, `tableAccent`,
`visualStyles`, `textClasses`, `outspaceColor`, `borderColor`, `shapeColors`

Always use `pbi report diff-theme` to preview changes before applying, and
open the report in Desktop once to confirm it loads before committing the file.

## Conditional Formatting

Apply data-driven formatting to individual visuals. Under the Orange style it is
used on tables and matrices only, with these two colour rules:
- **Highlight good or target cells** with the accent tint `#FFF1E5`.
- **Scales** go from `#FFFFFF` to `#FF7900`. This is the only gradient allowed.

Red/green traffic lights and any other colours are not part of the style.

```bash
# Gradient background (Orange scale: white -> orange)
pbi format background-gradient viz_1 --page synthese \
    --table Sales --column Revenue \
    --min-color "#FFFFFF" --max-color "#FF7900"

# Rules-based background (target reached -> accent tint)
pbi format background-conditional viz_1 --page synthese \
    --table Sales --column Status --value "Objectif atteint" --color "#FFF1E5"

# Measure-driven background (a DAX measure returns the colour)
pbi format background-measure visual_abc --page page1 \
    --table Sales --measure "Status Color"

# Inspect current formatting rules
pbi format get visual_abc --page page1

# Clear all formatting rules on a visual
pbi format clear visual_abc --page page1
```

## Workflow: Apply the Orange Brand

```bash
# 1. Write orange-dashboard-theme.json with the exact JSON from
#    power-bi-orange-dashboard (do not edit colours or fonts)

# 2. On an existing report, preview what changes first
pbi report diff-theme --file orange-dashboard-theme.json

# 3. Apply it
pbi report set-theme --file orange-dashboard-theme.json

# 4. Verify: custom_theme must be "Orange Dashboard"
pbi --json report get-theme

# 5. Restyling an existing report: set "width": 1920 / "height": 1080 in each
#    page.json (no CLI command resizes an existing page), run set-background
#    "#EFEFEF", then move visuals onto the Orange grid and add the page anatomy
#    (power-bi-pages, power-bi-orange-dashboard)
```

## JSON Output

```bash
pbi --json report get-theme
pbi --json report diff-theme --file proposed.json
pbi --json format get vis1 --page p1
```
