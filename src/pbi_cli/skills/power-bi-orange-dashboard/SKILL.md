---
name: Power BI Orange Dashboard
description: >
  Senior dashboard-design standard for every Power BI dashboard built with
  pbi-cli, in the Orange brand. Combines international standards (IBCS
  notation, WCAG 2.2 AA accessibility, Microsoft Power BI report-design
  guidance, Few/Tufte data-ink principles) with the Orange identity: #FF7900
  accent, Arial, white tiles on a #EFEFEF canvas, 8-pt grid, black footer band
  and a locked "Orange Restricted" label on every sheet. Invoke this skill FIRST
  whenever the user asks to build, design, brand, restyle, review or audit a
  dashboard, KPI tiles, executive overview, scorecard or "tableau de bord", or
  says "Orange style", "house style", "charte graphique". The other report
  skills supply the commands.
tools: pbi-cli
---

# Power BI Orange Dashboard — Design Standard

Work as a senior dashboard designer. A dashboard is a decision tool, not a
poster. Every pixel has to help a named reader answer a known question in
seconds. This standard combines the following, and resolves their conflicts
in favour of **legibility and truth first, brand second**:

| Standard | What it governs here |
|---|---|
| **IBCS** (International Business Communication Standards: SAY, UNIFY, CONDENSE, CHECK, EXPRESS, SIMPLIFY, STRUCTURE) | Titles, units, scenario notation, chart choice, scaling |
| **WCAG 2.2 AA** / Microsoft accessible-report guidance | Contrast, colour independence, alt text, tab order, minimum text size |
| **Microsoft Power BI design guidance** | Visual budget per page, slicer use, interaction, performance |
| **Few / Tufte** (data-ink, 5-second rule) | Remove chart junk; label directly; one glance shows the status |
| **Orange brand** (deck style "Modèle Churn Recharge", "Google My Business") | Colours, Arial, flat rectangles, the orange accent bar, black band |

## 1. Non-negotiables

1. **One page, one question.** Each page answers one question for one audience.
   If the question can't be written in one sentence, the page isn't designed yet.
2. **Five-second rule.** The status (good or bad, up or down, on target or not)
   is readable in 5 s from the top-left KPI band.
3. **No number without context.** Every KPI shows a comparison (vs previous year, budget or
   target) and its unit and period.
4. **Titles state measure, unit and period** (IBCS): "Chiffre d'affaires · M MAD · 2025 vs 2024".
5. **Same thing, same look** (IBCS UNIFY). A scenario, measure or category has
   one colour and one format across all pages.
6. **Contrast first.** All text meets WCAG AA. Orange `#FF7900` **text**
   appears only on black (`#111111`). On white or grey, orange is used only
   for bars, lines and accent bars, never for text.
7. **Never rely on colour alone.** Data labels, signs (+/−) and words carry the
   meaning; colour reinforces it.
8. **Truthful scales.** Bar and column axes start at zero. Charts that are
   compared share one scale. No 3D, no dual axes with unrelated units, no pie
   with more than 2 slices.
9. **Budget:** at most **8 data visuals per page**, KPI cards included, and at most 2 slicers.
   More is a second page or a drillthrough.
10. **The `Orange Restricted` label is on every page and is never touched** (§13).

## 2. Design process (do this before any command)

1. **Brief.** Write down, and confirm with the user if it is unclear:
   - the audience: executive, manager or analyst;
   - the decision the page supports;
   - the refresh cadence;
   - the 3–4 KPIs;
   - the comparison basis: PY, budget or target.
2. **Classify the page:**
   - *Strategic* (executive): KPIs and trends, few details, no tables.
   - *Operational* (manager): KPIs, breakdowns and exceptions, plus one table of exceptions.
   - *Analytical* (analyst): slicers, scatter or matrix, drillthrough.
3. **Inventory the model.** Run `pbi --json table list`, `pbi --json measure list` and
   `pbi --json column list -t <table>`. Create missing measures with format
   strings (power-bi-modeling). Multi-line DAX goes through `-e -` and stdin, never inline.
4. **Wireframe in text first.** List each zone (§6) with its visual type and
   fields, and check it against the chart chooser (§7) and the budget (§1.9).
5. **Build** in reading order (§12). Reading order becomes the keyboard tab order.
6. **Review** with the scorecard in §14 before reporting back.

## 3. Colour system

| Token | Hex | Role | Allowed as text on |
|---|---|---|---|
| Orange (Accent) | `#FF7900` | Focus: the primary measure (AC), accent bars, insight stripe, page number, classification label | **Black only** (7.18:1) |
| Ink | `#111111` | Titles, KPI values, body text, footer band, PL/target lines | White 18.9:1 · canvas 16.4:1 · tint 17.1:1 |
| Body | `#555555` | Secondary text, axes, PY series | White 7.5:1 · canvas 6.5:1 |
| Mid grey | `#9A9A9A` | Tertiary series and gridless context | Not for text (2.8:1) |
| Canvas | `#EFEFEF` | Page background; text on black (16.4:1) | — |
| Card | `#FFFFFF` | Every data tile | — |
| Accent tint | `#FFF1E5` | Insight bar background, highlighted cells | — |
| Stage colours | `#A8683A` `#D9A400` | Only for staged processes (Bronze/Gold) | — |

**Semantic rules**
- **Orange means "look here".** It is used for the primary measure (AC), the
  accent bars of at most 2 focus KPIs per page, the insight stripe, the page number and the label.
  Never use it for "bad" and never as decoration.
- **Scenario notation (IBCS, adapted to the brand):**
  - AC (actual) = `#FF7900`;
  - PY (previous year) = `#555555`;
  - PL/BU (plan or budget) = `#111111`, as a line or target marker;
  - FC (forecast) = `#9A9A9A`, and always with data labels.
  Apply the same mapping on every visual.
- **Separating series:** `#FF7900` and `#9A9A9A` have the same lightness
  (1.07:1), so colour-blind readers and greyscale prints cannot tell them apart. Never let
  them be the only difference between two adjacent series. For two series use orange + `#555555`; for three,
  orange + `#555555` + `#111111`.
- **Variance:** show the sign (+/−) and the value; colour is optional. No red/green.
  Unfavourable variances may be highlighted with the accent tint `#FFF1E5` in
  tables.
- **At most 4 colours in any chart.** Beyond that, use small multiples or "Others".

## 4. Typography (Arial only; Power BI points on a 1920×1080 page)

| Role | Size | Weight | Colour |
|---|---|---|---|
| Page title | 28 pt | bold | `#111111` |
| Kicker (section · subsection, UPPERCASE) | 12 pt | bold | `#555555` |
| KPI value | 32 pt | bold | `#111111` |
| KPI label | 12 pt | bold | `#111111` |
| KPI comparison | 12 pt | regular | `#555555` |
| Visual title | 14 pt | bold | `#111111` |
| Axis, data labels, legend, table body | 12 pt | regular | `#555555` |
| Table headers | 12 pt | bold | `#111111` |
| Insight text | 16 pt | bold | `#111111` on `#FFF1E5` |
| Footer text | 12 pt | regular | `#EFEFEF` on `#111111` |
| Page number | 14 pt | bold | `#FF7900` on `#111111` |
| Orange Restricted label | 12 pt | bold | `#FF7900` on `#111111` (fixed by pbi-cli) |

Never go below 12 pt. Use sentence case for all titles; uppercase only for the kicker.
At most 3 sizes in the body zone.

## 5. Grid

The canvas is **1920×1080**, display option FitToPage. The grid is built on **8 pt**: outer margin
**48**, gutter **16**, and every y coordinate is a multiple of 8. Readers scan in a **Z pattern**:
status top-left, detail in the middle, the "so what" at the bottom.

```
y   0 ┌────────────────────────────────────────────────────────────┐
 32   ▬ orange accent bar                         [slicer][slicer] │ HEADER
 48   KICKER · SUBSECTION                                          │
 72   Page title: measure · unit · period                          │
152   [ KPI 1 ][ KPI 2 ][ KPI 3 ][ KPI 4 ]                         │ KPI BAND
320   ┌──────── visual ────────┐┌──────── visual ────────┐         │ BODY
      │                        ││                        │         │
896   └────────────────────────┘└────────────────────────┘         │
920   ▌ Insight: what it means and what to do                      │ INSIGHT
1008 ███ footer · source · data as of ███ Orange Restricted ██ 01 ███│ FOOTER BAND
1080 └────────────────────────────────────────────────────────────┘
```

## 6. Zones, components and exact positions

Positions are `x, y, w, h` in px. Use these names: they set the tab order and make
reviews and bulk edits possible.

**Header (y 32–128)**

| Name | Component | x | y | w | h |
|---|---|---|---|---|---|
| `hdr_accent` | shape `#FF7900` (brand bar) | 48 | 32 | 96 | 8 |
| `hdr_kicker` | textbox, 12 pt bold `#555555` UPPERCASE | 48 | 48 | 1264 | 24 |
| `hdr_title` | textbox, 28 pt bold `#111111` | 48 | 72 | 1264 | 48 |
| `slc_1`, `slc_2` | slicer (dropdown) | 1328 / 1608 | 48 | 264 | 80 |

Without slicers, `hdr_kicker` and `hdr_title` widen to w 1824. The title is the
**page purpose, which is always true** ("Performance commerciale · M MAD · cumul
annuel"). The message goes in the insight bar.

**KPI band (y 152–296)**: 3 or 4 tiles. Each tile is a value card, with a comparison card underneath and touching it.

| Layout | x positions | w | value card `kpi_n` | comparison `kpi_n_cmp` |
|---|---|---|---|---|
| 4 tiles | 48 / 508 / 968 / 1428 | 444 | y 152, h 112 | y 264, h 32 |
| 3 tiles | 48 / 661 / 1274 | 597 (last 598) | y 152, h 112 | y 264, h 32 |

- The comparison card is bound to a text measure such as `"+4,2 % vs A-1"` or `"−1,3 pt vs objectif"`. Use a static textbox only if no measure can be created.
- **Focus KPI accent:** for at most 2 tiles, add `kpi_n_accent`, an orange shape at the tile's x, y 152, w = tile width, h 8. It is added after the tile so it sits on top.
- KPI values stay `#111111`. **Never colour a KPI value orange** (contrast 2.6:1).

**Body (y 320–896, h 576)**

| Layout | x | w |
|---|---|---|
| 2 halves `viz_1`, `viz_2` | 48 / 968 | 904 |
| 3 thirds `viz_1`…`viz_3` | 48 / 661 / 1274 | 597 / 597 / 598 |
| 2/3 + 1/3 | 48 / 1269 | 1205 / 603 |
| 2×2 small multiples | 48 / 968; y 320 / 616 | 904, h 280 |

**Insight bar (y 920–984)**

| Name | Component | x | y | w | h |
|---|---|---|---|---|---|
| `ins_stripe` | shape `#FF7900` | 48 | 920 | 8 | 64 |
| `ins_text` | card bound to an insight measure (dynamic), or a textbox; background `#FFF1E5`, 16 pt bold `#111111` | 56 | 920 | 1816 | 64 |

The insight is one sentence: *what happened + so what*. If the page has slicers
or refreshes, the insight **must be dynamic** (a card bound to a DAX text measure),
so it never contradicts the data on screen. A static insight is allowed only on
a fixed snapshot, and its numbers come from `pbi dax execute`.

**Footer band (y 1008–1080, full bleed)**

| Name | Component | x | y | w | h |
|---|---|---|---|---|---|
| `ftr_band` | shape `#111111` | 0 | 1008 | 1920 | 72 |
| `ftr_left` | textbox 12 pt `#EFEFEF`: dashboard · source · "données au JJ/MM/AAAA" | 48 | 1028 | 1196 | 36 |
| `cls_restricted` | **automatic, read-only** "Orange Restricted" | 1268 | 1028 | 364 | 36 |
| `ftr_page` | textbox 14 pt bold `#FF7900`, right-aligned: `01`, `02`… | 1672 | 1028 | 200 | 36 |

## 7. Chart chooser

| Question | Use | Rules |
|---|---|---|
| How are we doing vs PY/target? | `card` + comparison card | Value + comparison + unit, always |
| Ranking / structure (categories) | `bar` (horizontal) | Sorted descending, data labels on, value axis hidden, ≤ 12 bars (Top N + "Autres") |
| Evolution over periods | `column` (≤ 13 periods) or `line` (> 13 periods) | Time runs left → right; IBCS: columns for periods, lines for long series |
| Actual vs plan over time | `combo` | AC as columns in orange, PL as a `#111111` line; one unit |
| Bridge / contribution | `waterfall` | Start and end totals `#111111`, increases `#555555`, decreases orange with labels |
| Two-measure relationship | `scatter` | Analytical pages only; label outliers |
| Exceptions / detail | `table`, `matrix` | ≤ 7 columns, numbers right-aligned, highlight with the tint |
| Composition of 2 parts | `bar` (100 %) or a sentence | Never pie or donut with more than 2 slices |

**Not allowed unless the user explicitly asks:** pie/donut, gauge, treemap, ribbon, funnel,
maps, the `kpi` visual, 3D, images, decorative icons, page navigators, action buttons.
Explain why (legibility, comparison accuracy) and offer the alternative from the table above.

**Data-ink:** gridlines off, axis titles off (the unit is in the visual title),
the legend only when there are 2 or more series, at the top-left, or direct labels instead. No borders,
shadows or rounded corners; the theme enforces this.

## 8. Numbers and text

- Match the user's language. **French:** `677 336`, `82,7 %`, `1,85×`, `12,4 M MAD`;
  **English:** `677,336`, `82.7%`.
- Use 3 significant digits on KPIs (`12,4 M`), at most 1 decimal on percentages, and
  the same decimals throughout a column or axis.
- Put the unit in the title, not on every label ("en M MAD"). Write negatives with a minus sign,
  and variances with an explicit sign (`+4,2 %`, `−1,3 pt`).
- Use dates in the reader's format (`JJ/MM/AAAA` in French). Periods: `T1 2025`, `janv. 2025`.
- Use plain language in KPI labels ("Clients perdus", not "churn_flag_sum").

## 9. Interaction

- Slicers: at most 2, in the header slots, as dropdowns (the theme sets this). Use them only for dimensions
  the audience really changes, such as period or region. Prefer page filters for fixed scope.
- If a filter changes what the page shows, the scope must be visible in the
  title or footer ("Top 10 produits", "30 derniers jours").
- Cross-filtering stays on (default). Detail belongs in **drillthrough pages**
  (hidden, same grid, no insight bar needed), not on the main page.
- Every visual gets a tooltip-friendly title. Never hide meaning in hover-only content.

## 10. Accessibility (WCAG 2.2 AA)

- The contrast table in §3 is binding. Text sizes are ≥ 12 pt.
- **Alt text on every data visual:** what it shows and the main takeaway (recipe in §12).
- **Tab order = reading order.** pbi-cli sets tab order in creation order, so build
  header → KPIs → body → insight → footer.
- Line charts with 2 or more series need markers or direct labels. Bar charts need data labels.
- Colour is never the only carrier of meaning (§1.7).

## 11. The theme (apply once per report)

Write the file exactly as shown, then run
`pbi report --no-sync set-theme --file orange-dashboard-theme.json`:

```json
{
  "name": "Orange Dashboard",
  "dataColors": ["#FF7900", "#555555", "#111111", "#9A9A9A", "#A8683A", "#D9A400"],
  "background": "#FFFFFF",
  "foreground": "#111111",
  "tableAccent": "#FF7900",
  "good": "#555555",
  "neutral": "#9A9A9A",
  "bad": "#FF7900",
  "minimum": "#FFFFFF",
  "maximum": "#FF7900",
  "textClasses": {
    "callout": { "fontSize": 32, "fontFace": "Arial", "color": "#111111" },
    "title": { "fontSize": 14, "fontFace": "Arial", "color": "#111111" },
    "header": { "fontSize": 12, "fontFace": "Arial", "color": "#111111" },
    "label": { "fontSize": 12, "fontFace": "Arial", "color": "#555555" }
  },
  "visualStyles": {
    "*": {
      "*": {
        "background": [{ "show": true, "color": { "solid": { "color": "#FFFFFF" } }, "transparency": 0 }],
        "border": [{ "show": false }],
        "dropShadow": [{ "show": false }],
        "visualHeader": [{ "show": false }],
        "title": [{
          "show": true, "fontFamily": "Arial", "fontSize": 14, "bold": true,
          "fontColor": { "solid": { "color": "#111111" } }, "alignment": "left"
        }],
        "categoryAxis": [{
          "fontFamily": "Arial", "fontSize": 12,
          "labelColor": { "solid": { "color": "#555555" } }, "showAxisTitle": false
        }],
        "valueAxis": [{
          "fontFamily": "Arial", "fontSize": 12,
          "labelColor": { "solid": { "color": "#555555" } },
          "gridlineShow": false, "showAxisTitle": false
        }],
        "labels": [{ "fontFamily": "Arial", "fontSize": 12, "color": { "solid": { "color": "#555555" } } }],
        "legend": [{
          "show": true, "position": "Top", "fontFamily": "Arial", "fontSize": 12,
          "labelColor": { "solid": { "color": "#555555" } }
        }]
      }
    },
    "page": {
      "*": {
        "background": [{ "color": { "solid": { "color": "#EFEFEF" } }, "transparency": 0 }],
        "outspace": [{ "color": { "solid": { "color": "#EFEFEF" } }, "transparency": 0 }]
      }
    },
    "barChart": { "*": { "labels": [{ "show": true }], "valueAxis": [{ "show": false }] } },
    "clusteredBarChart": { "*": { "labels": [{ "show": true }], "valueAxis": [{ "show": false }] } },
    "columnChart": { "*": { "labels": [{ "show": true }], "valueAxis": [{ "show": false }] } },
    "clusteredColumnChart": { "*": { "labels": [{ "show": true }], "valueAxis": [{ "show": false }] } },
    "waterfallChart": {
      "*": {
        "labels": [{ "show": true }],
        "sentimentColors": [{
          "increaseFill": { "solid": { "color": "#555555" } },
          "decreaseFill": { "solid": { "color": "#FF7900" } },
          "totalFill": { "solid": { "color": "#111111" } }
        }]
      }
    },
    "card": {
      "*": {
        "title": [{ "show": false }],
        "labels": [{ "fontFamily": "Arial", "fontSize": 32, "color": { "solid": { "color": "#111111" } } }],
        "categoryLabels": [{ "show": true, "fontFamily": "Arial", "fontSize": 12, "color": { "solid": { "color": "#111111" } } }]
      }
    },
    "tableEx": {
      "*": {
        "columnHeaders": [{ "fontFamily": "Arial", "fontSize": 12, "bold": true,
          "fontColor": { "solid": { "color": "#111111" } }, "backColor": { "solid": { "color": "#FFFFFF" } } }],
        "values": [{ "fontFamily": "Arial", "fontSize": 12,
          "fontColorPrimary": { "solid": { "color": "#555555" } }, "backColorPrimary": { "solid": { "color": "#FFFFFF" } },
          "fontColorSecondary": { "solid": { "color": "#555555" } }, "backColorSecondary": { "solid": { "color": "#FFFFFF" } } }],
        "total": [{ "fontFamily": "Arial", "fontSize": 12, "bold": true,
          "fontColor": { "solid": { "color": "#111111" } }, "backColor": { "solid": { "color": "#EFEFEF" } } }],
        "grid": [{ "gridHorizontal": true, "gridHorizontalColor": { "solid": { "color": "#EFEFEF" } }, "gridVertical": false }]
      }
    },
    "pivotTable": {
      "*": {
        "columnHeaders": [{ "fontFamily": "Arial", "fontSize": 12, "bold": true,
          "fontColor": { "solid": { "color": "#111111" } }, "backColor": { "solid": { "color": "#FFFFFF" } } }],
        "rowHeaders": [{ "fontFamily": "Arial", "fontSize": 12, "bold": true,
          "fontColor": { "solid": { "color": "#111111" } }, "backColor": { "solid": { "color": "#FFFFFF" } } }],
        "values": [{ "fontFamily": "Arial", "fontSize": 12,
          "fontColorPrimary": { "solid": { "color": "#555555" } }, "backColorPrimary": { "solid": { "color": "#FFFFFF" } },
          "fontColorSecondary": { "solid": { "color": "#555555" } }, "backColorSecondary": { "solid": { "color": "#FFFFFF" } } }],
        "subTotals": [{ "fontFamily": "Arial", "fontSize": 12, "bold": true,
          "fontColor": { "solid": { "color": "#111111" } }, "backColor": { "solid": { "color": "#EFEFEF" } } }],
        "grid": [{ "gridHorizontal": true, "gridHorizontalColor": { "solid": { "color": "#EFEFEF" } }, "gridVertical": false }]
      }
    },
    "slicer": {
      "*": {
        "data": [{ "mode": "Dropdown" }],
        "header": [{ "fontFamily": "Arial", "fontSize": 12, "bold": true, "fontColor": { "solid": { "color": "#111111" } } }],
        "items": [{ "fontFamily": "Arial", "fontSize": 12, "fontColor": { "solid": { "color": "#555555" } } }]
      }
    },
    "textbox": { "*": { "background": [{ "show": false }], "title": [{ "show": false }] } },
    "shape": { "*": { "background": [{ "show": false }], "title": [{ "show": false }] } }
  }
}
```

Do not add `radius`, a top-level `page` key or `dropShadow.position` (see
power-bi-themes). Never apply another theme to an Orange dashboard.

## 12. Build recipes

`pbi visual add` creates `definition/pages/<page>/visuals/<name>/visual.json`.
No CLI command sets textbox text, shape fill, card text styling or alt text.
For those, edit the `"visual"` object in the file and keep `$schema`, `name`,
`position` and any `query` written by `pbi visual bind`. Run `pbi report validate`
after each batch.

**Textbox** (kicker, title, static insight, footer text, page number):

```json
"visual": {
  "visualType": "textbox",
  "objects": {
    "general": [{
      "properties": {
        "paragraphs": [{
          "textRuns": [
            { "value": "Performance commerciale", "textStyle": { "fontFamily": "Arial", "fontSize": "28pt", "fontWeight": "bold", "color": "#111111" } }
          ]
        }]
      }
    }]
  },
  "visualContainerObjects": {
    "background": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]
  },
  "drillFilterOtherVisuals": true
}
```

Apply sizes and colours from §4. For the page number, add
`"horizontalTextAlignment": "right"` to the paragraph.

**Rectangle shape** (`hdr_accent`, `kpi_n_accent`, `ins_stripe` in `#FF7900`;
`ftr_band` in `#111111`):

```json
"visual": {
  "visualType": "shape",
  "objects": {
    "shape": [{ "properties": { "tileShape": { "expr": { "Literal": { "Value": "'rectangle'" } } } } }],
    "fill": [{
      "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FF7900'" } } } } },
        "transparency": { "expr": { "Literal": { "Value": "0D" } } }
      },
      "selector": { "id": "default" }
    }],
    "outline": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]
  },
  "visualContainerObjects": {
    "background": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]
  },
  "drillFilterOtherVisuals": true,
  "howCreated": "InsertVisualButton"
}
```

**Dynamic text card** (`kpi_n_cmp`, `ins_text`). Bind it to a text measure with
`pbi visual bind <name> --page <page> --field "_Mesures[Insight Synthèse]"`,
then add the following to its `"visual"` object. Use `16D` and the `#FFF1E5`
background for the insight, and `12D` with `#555555` text and a `#FFFFFF`
background for comparison cards.

```json
"objects": {
  "labels": [{ "properties": {
    "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#111111'" } } } } },
    "fontSize": { "expr": { "Literal": { "Value": "16D" } } },
    "fontFamily": { "expr": { "Literal": { "Value": "'Arial'" } } }
  } }],
  "categoryLabels": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
  "wordWrap": [{ "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } }]
},
"visualContainerObjects": {
  "background": [{ "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FFF1E5'" } } } } },
    "transparency": { "expr": { "Literal": { "Value": "0D" } } }
  } }]
}
```

Example insight measure (save to `insight.dax`, then run
`pbi measure create "Insight Synthèse" -t _Mesures -e - < insight.dax`):

```
VAR ac = [CA]
VAR py = [CA A-1]
VAR d  = DIVIDE ( ac - py, py )
RETURN
    "Le chiffre d'affaires " & IF ( d >= 0, "progresse de ", "recule de " )
        & FORMAT ( ABS ( d ), "0.0 %" ) & " vs A-1 : "
        & IF ( d >= 0, "maintenir l'effort sur les régions leaders.", "prioriser les régions en recul." )
```

**Alt text.** Merge this into the visual's `visualContainerObjects`:

```json
"general": [{ "properties": { "altText": { "expr": { "Literal": { "Value": "'Barres : CA 2025 par région, Casablanca en tête'" } } } } }]
```

**Secondary chart in grey** (keeps orange for the focus chart). Add this to the `"visual"` object:

```json
"objects": { "dataPoint": [{ "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#555555'" } } } } } } }] }
```

**Visual title.** Every data visual gets one:
`pbi visual --no-sync set-container viz_1 --page synthese --title "CA par région · M MAD · 2025"`.

**Build sequence.** Building in reading order gives the keyboard tab order:

```bash
pbi report create . --name "Ventes" --dataset-path "../Ventes.SemanticModel"
pbi report --no-sync set-theme --file orange-dashboard-theme.json
pbi report --no-sync add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report --no-sync set-background synthese --color "#EFEFEF"   # label cls_restricted is added automatically

V="pbi visual --no-sync"; P="--page synthese"
$V add $P --type shape   --name hdr_accent --x 48 --y 32 --width 96   --height 8
$V add $P --type textbox --name hdr_kicker --x 48 --y 48 --width 1264 --height 24
$V add $P --type textbox --name hdr_title  --x 48 --y 72 --width 1264 --height 48
$V add $P --type slicer  --name slc_1 --x 1328 --y 48 --width 264 --height 80
for i in 1 2 3 4; do x=$((48 + (i-1)*460))
  $V add $P --type card --name kpi_$i     --x $x --y 152 --width 444 --height 112
  $V add $P --type card --name kpi_${i}_cmp --x $x --y 264 --width 444 --height 32
done
$V add $P --type shape --name kpi_1_accent --x 48 --y 152 --width 444 --height 8
$V add $P --type bar   --name viz_1 --x 48  --y 320 --width 904 --height 576
$V add $P --type combo --name viz_2 --x 968 --y 320 --width 904 --height 576
$V add $P --type shape --name ins_stripe --x 48 --y 920 --width 8    --height 64
$V add $P --type card  --name ins_text   --x 56 --y 920 --width 1816 --height 64
$V add $P --type shape   --name ftr_band --x 0    --y 1008 --width 1920 --height 72
$V add $P --type textbox --name ftr_left --x 48   --y 1028 --width 1196 --height 36
$V add $P --type textbox --name ftr_page --x 1672 --y 1028 --width 200  --height 36
# bind data, titles, then the JSON recipes; finally:
pbi report validate --full
pbi report reload
```

## 13. Orange Restricted label (mandatory, read-only)

Every page carries the classification label **`Orange Restricted`** (Arial 12 pt
bold, `#FF7900`), a textbox named `cls_restricted` in the footer band at
x 1268, y 1028, 364×36. On the black band it meets contrast (7.18:1).

- `pbi report add-page` inserts it automatically, and it always stays above other visuals.
- Every pbi-cli write command (`visual add/update/delete/bind/set-container`,
  `format …`, `filters … --visual`, `calc-…`) refuses `cls_restricted`; the
  bulk commands skip it.
- `pbi report validate` (and `--full`) fails if a page lacks the label or its
  text, colour, visibility or size changed. `pbi report apply-classification [PAGE]`
  restores it. Use that command on reports created elsewhere.
- Never edit `visuals/cls_restricted/visual.json` by hand, and never put a visual over
  its slot.
- If the user asks to remove, rename, recolour or hide it, decline: it is a mandatory
  classification marking. It can only be changed in
  `pbi_cli/core/classification.py` by the toolkit's maintainers.

## 14. Design review scorecard

Score each line as pass or fail before reporting back, and report any failures with a fix.
Use the same scorecard when the user asks for a review of an existing dashboard.

| # | Check | Standard |
|---|---|---|
| 1 | One question per page; the title states measure · unit · period | IBCS SAY / EXPRESS |
| 2 | Status readable in 5 s from the KPI band; every KPI has a comparison | Few |
| 3 | ≤ 8 data visuals and ≤ 2 slicers per page | Microsoft guidance |
| 4 | Positions match the grid in §6; nothing overlaps; 48 margin and 16 gutter | Orange grid |
| 5 | Only approved chart types; bars sorted; zero-based axes; ≤ 4 colours | IBCS / Tufte |
| 6 | Scenario colours consistent (AC orange, PY `#555555`, PL `#111111`) | IBCS UNIFY |
| 7 | No orange text outside the black band; all text ≥ 12 pt | WCAG 1.4.3 |
| 8 | Meaning never by colour alone; labels or signs present | WCAG 1.4.1 / 1.4.11 |
| 9 | Alt text on every data visual; build order = reading order | WCAG / Microsoft |
| 10 | Numbers in the user's locale; units in titles; consistent decimals | IBCS CONDENSE |
| 11 | Insight is dynamic when the page has slicers; numbers verified by DAX | Truthfulness |
| 12 | Orange theme applied (`pbi --json report get-theme`) | Brand |
| 13 | `Orange Restricted` present and untouched on every page | Classification |
| 14 | `pbi report validate --full` passes; report opens after `pbi report reload` | Technical |
