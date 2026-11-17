---
name: Power BI Orange Dashboard
description: >
  House design system for every Power BI dashboard built with pbi-cli: Orange
  #FF7900 accent, Arial, flat white tiles on a #EFEFEF canvas, conclusion
  headline, black takeaway bar, numbered footer, and a locked "Orange
  Restricted" label on every sheet. Invoke this
  skill FIRST whenever the user asks to build, design, brand, restyle or review
  a dashboard, KPI tiles, executive overview or scorecard, or says "Orange
  style", "house style", "charte graphique", "tableau de bord". Every layout,
  visual, theme and colour decision must follow it. The other report skills
  supply the commands.
tools: pbi-cli
---

# Power BI Orange Dashboard Skill

This repository produces **one kind of output: Power BI dashboards in the Orange
house style**. The style is the presentation style used for the decks "Modèle
Churn Recharge – Performance" and "Google My Business – Avis Google Maps",
transposed to a Power BI page. Apply it exactly. Do not invent colours, fonts,
layouts or visual types. If the user asks for a different look, say that this
toolkit is locked to the Orange style and ask before deviating.

## Workflow

1. **Gather the content first.** Read the model with `pbi --json table list`,
   `pbi --json measure list` and `pbi --json column list -t <table>`. Decide the
   one message of each page before placing anything.
2. **Compute every number in code; never estimate.** Any figure written into a
   headline, KPI caption or takeaway bar comes from a `pbi dax execute` result.
   Measures behind KPI tiles must exist (see power-bi-modeling) and carry a
   format string.
3. **Scaffold** (power-bi-report): `pbi report create`, then write the theme
   below to `orange-dashboard-theme.json` and `pbi report --no-sync set-theme`.
4. **Add pages at 1920×1080** with the `#EFEFEF` background (power-bi-pages).
5. **Place the page anatomy** using the grid coordinates below, with fixed
   visual names (power-bi-visuals). Use `--no-sync` on every write.
6. **Write the text and shape recipes** into each decorative `visual.json`
   (no CLI command sets textbox text or shape fill; edit the JSON directly).
7. **Validate and reload:** `pbi report validate`, then `pbi report reload` once.
8. **Run the checklist** at the end of this file before reporting back.

Language: match the user's request and source material (past work is in
French). In French dashboards use French number formatting: `677 336`,
`82,7 %`, `0,8591`, `1,85×`. For measures, use format strings such as
`#,0` with the French culture, `0.0 %` and `0.0000`.

## Design tokens

| Token | Value | Use |
|---|---|---|
| Accent | `#FF7900` | Kicker topic, hero KPI values (max 2 per row), page number, key-metric series, takeaway stripe |
| Ink | `#111111` | Headline, tile labels, visual titles, takeaway bar, secondary KPI values |
| Body | `#555555` | Kicker, captions, axis labels, footer, secondary series |
| Canvas | `#EFEFEF` | Page background, table grid lines, neutral cells |
| Card | `#FFFFFF` | Every data visual's background (tile) |
| Accent tint | `#FFF1E5` | Highlighted good/target cells in tables and matrices |
| Stage colours | `#A8683A` `#9A9A9A` `#D9A400` | Only when stages have their own identity (Bronze/Silver/Gold) |
| Font | `Arial` | Everything. Bold for titles and numbers, regular for body |

**Forbidden:** rounded corners, shadows, gradients (except the conditional-
formatting scale defined below), icons, emoji, photos (unless the user supplies
them), visual headers and borders. Use flat rectangles only. Use orange sparingly: the kicker topic, at most 2
hero values per KPI row, the key series of at most 2 charts per page, the
takeaway stripe and the page number.

### Type scale (Power BI points, on a 1920×1080 page)

The deck is specified in px on a 1920 canvas. A dashboard is denser, so the
hierarchy is kept but scaled down. No text is smaller than 12 pt.

| Element | Size | Weight | Colour |
|---|---|---|---|
| Kicker (UPPERCASE text) | 14 pt | bold | topic `#FF7900` · subtopic `#555555` |
| Headline | 32 pt | bold | `#111111` |
| Hero KPI value | 36 pt | bold | `#FF7900` (max 2 per row), others `#111111` |
| KPI label | 14 pt | bold | `#111111` |
| KPI caption / plain-language meaning | 12 pt | regular | `#555555` |
| Visual title | 14 pt | bold | `#111111` |
| Axis, data labels, table body | 12 pt | regular | `#555555` |
| Table / matrix headers | 12 pt | bold | `#111111` |
| Takeaway bar text | 18 pt | bold | `#FFFFFF`, key figure optional `#FF7900` |
| Footer | 12 pt | regular | `#555555` |
| Page number | 14 pt | bold | `#FF7900` |

## Page anatomy (every dashboard page)

1. **Kicker**: `TOPIC · SUBTOPIC` in uppercase, with the topic in orange.
2. **Headline**: one sentence stating the conclusion in ≤ 12 words ("Le
   modèle détecte 5 churners sur 6", not "Performance").
3. **KPI row**: 3 or 4 white tiles (card visuals). Each tile shows a value,
   a label and, optionally, a 12 pt caption with the plain-language meaning.
4. **Body**: 2 or 3 white data visuals, one idea each.
5. **Takeaway bar**: a black bar with a 12 px orange left stripe and one white bold
   sentence giving the business implication.
6. **Footer**: dashboard name · context · data date on the left, the
   **Orange Restricted** classification label, and the two-digit page number
   `01`, `02`… in bold orange on the right.

## Orange Restricted label (mandatory, read-only)

Every page of every dashboard carries the classification label
**`Orange Restricted`**: Arial 12 pt bold, `#FF7900`, right-aligned in the footer
slot, as a textbox named `cls_restricted`. It is **not** part of your design work,
and you never write, edit, move, recolour, resize, hide, reword or delete it.

- `pbi report add-page` inserts it automatically on every new page.
- Every pbi-cli write command (`visual add/update/delete/bind/set-container`,
  `format …`, `filters … --visual`, `calc-…`) refuses to target
  `cls_restricted`, and the bulk commands skip it.
- `pbi report validate` (and `--full`) fails when a page is missing the label or
  its text, colour or visibility has been altered.
- `pbi report apply-classification [PAGE]` restores the canonical label, on all
  pages when PAGE is omitted. Run it on reports created by another tool and
  whenever validation reports a label problem.
- Never edit `visuals/cls_restricted/visual.json` by hand, and never place
  another visual over the label's slot.
- If the user asks to remove, rename, recolour or hide it, decline: it is a
  mandatory classification marking that this toolkit locks. The label text and
  colour are fixed in `pbi_cli/core/classification.py` and can only be changed
  there by the toolkit's maintainers.

## Layout grid (1920×1080, outer margin 64 px, gap 24 px)

Positions are `x, y, width, height` in pixels. Use these exact values and visual names.

| Name | Type | x | y | w | h |
|---|---|---|---|---|---|
| `hdr_kicker` | textbox | 64 | 40 | 1792 | 40 |
| `hdr_headline` | textbox | 64 | 80 | 1792 | 64 |
| `kpi_1`…`kpi_4` (4 tiles) | card | 64 / 518 / 972 / 1426 | 168 | 430 | 152 |
| `kpi_1`…`kpi_3` (3 tiles) | card | 64 / 669 / 1274 | 168 | 581 (last 582) | 152 |
| `viz_1`, `viz_2` (halves) | chart/table | 64 / 972 | 344 | 884 | 572 |
| `viz_1`…`viz_3` (thirds) | chart/table | 64 / 669 / 1274 | 344 | 581 (last 582) | 572 |
| `viz_1` + `viz_2` (2/3 + 1/3) | chart/table | 64 / 1277 | 344 | 1189 / 579 | 572 |
| `tk_bar` | shape `#111111` | 64 | 940 | 1792 | 72 |
| `tk_stripe` | shape `#FF7900` | 64 | 940 | 12 | 72 |
| `tk_text` | textbox | 100 | 940 | 1732 | 72 |
| `ftr_left` | textbox | 64 | 1028 | 1180 | 36 |
| `cls_restricted` | **auto, read-only** "Orange Restricted" | 1268 | 1028 | 364 | 36 |
| `ftr_page` | textbox (right-aligned) | 1656 | 1028 | 200 | 36 |

Optional KPI captions go in `kpi_n_cap` textboxes laid over the bottom of each
tile: same x and width as the tile, y 284, h 32, added after the tile so they sit above it.

**Slicers:** at most 2 per page. They go top-right in the header (`slc_1` x 1296,
`slc_2` x 1588; y 48, w 268, h 88), and `hdr_kicker`/`hdr_headline` then shrink to
w 1208. The theme renders slicers as dropdowns. Do not place slicers in the body.

**Z-order:** `pbi visual add` stacks each new visual above the previous ones, so add
`tk_bar` → `tk_stripe` → `tk_text`, and add each tile before its caption.

## Approved visual types

| Purpose | Use | Notes |
|---|---|---|
| KPI tile | `card` | Default value colour `#111111`; recolour max 2 hero tiles orange (recipe below) |
| Ranking / comparison | `bar`, `clustered_bar` | Horizontal bars sorted descending (Desktop's default sort for a single measure) |
| Trend over time | `line`, `column`, `area` | Key series bound first so it takes `#FF7900` |
| Value + rate | `combo` | Columns = volume, line = rate |
| Contribution / bridge | `waterfall` | Use the theme's colours as they are |
| Correlation | `scatter` | Only for analytical pages |
| Detail | `table`, `matrix` | Highlight target cells with the accent-tint rule |
| Filtering | `slicer` | Header slots only |
| Decoration | `textbox`, `shape` | Only for the anatomy elements above |

**Not allowed unless the user explicitly asks:** pie/donut, gauge, treemap, ribbon,
funnel, maps, KPI visual (`kpi`), images, action buttons, page navigators and
custom visuals. Give the business reason, then offer the approved alternative:
a bar chart instead of pie/donut/treemap, a card plus caption instead of a gauge or KPI visual.

## The theme (apply once per report)

Write this file exactly as shown, then run
`pbi report --no-sync set-theme --file orange-dashboard-theme.json`:

```json
{
  "name": "Orange Dashboard",
  "dataColors": ["#FF7900", "#555555", "#111111", "#9A9A9A", "#A8683A", "#D9A400"],
  "background": "#FFFFFF",
  "foreground": "#111111",
  "tableAccent": "#FF7900",
  "textClasses": {
    "callout": { "fontSize": 36, "fontFace": "Arial", "color": "#111111" },
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
    "card": {
      "*": {
        "title": [{ "show": false }],
        "labels": [{ "fontFamily": "Arial", "fontSize": 36, "color": { "solid": { "color": "#111111" } } }],
        "categoryLabels": [{ "show": true, "fontFamily": "Arial", "fontSize": 14, "color": { "solid": { "color": "#111111" } } }]
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

## JSON recipes for decorative visuals

`pbi visual add` creates `definition/pages/<page>/visuals/<name>/visual.json`.
For the elements below, replace the `"visual"` object in that file with the
recipe, keeping `$schema`, `name` and `position` as they are.
Then run `pbi report validate`.

### Textbox (kicker, headline, takeaway text, footer, page number, captions)

```json
"visual": {
  "visualType": "textbox",
  "objects": {
    "general": [{
      "properties": {
        "paragraphs": [{
          "textRuns": [
            { "value": "VENTES", "textStyle": { "fontFamily": "Arial", "fontSize": "14pt", "fontWeight": "bold", "color": "#FF7900" } },
            { "value": " · PERFORMANCE RÉGIONALE", "textStyle": { "fontFamily": "Arial", "fontSize": "14pt", "fontWeight": "bold", "color": "#555555" } }
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

Change the text runs per element, using the type-scale table:
- **Headline:** one run, `32pt`, bold, `#111111`.
- **Takeaway text:** `18pt`, bold, `#FFFFFF`. An optional middle run in `#FF7900` holds the key figure.
- **Footer:** `12pt`, regular (omit `fontWeight`), `#555555`.
- **Page number:** `14pt`, bold, `#FF7900`. Add `"horizontalTextAlignment": "right"` to the paragraph.
- **KPI caption:** `12pt`, regular, `#555555`.

Text is static, so write the uppercase kicker as uppercase. Every number in it must
come from a DAX result, and the footer states the data date.

### Rectangle shape (takeaway bar `#111111`, stripe `#FF7900`)

```json
"visual": {
  "visualType": "shape",
  "objects": {
    "shape": [{ "properties": { "tileShape": { "expr": { "Literal": { "Value": "'rectangle'" } } } } }],
    "fill": [{
      "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#111111'" } } } } },
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

### Hero KPI tile in orange (max 2 per row)

Add this inside the card's `"visual"` object. Keep the `query` that
`pbi visual bind` wrote.

```json
"objects": {
  "labels": [{ "properties": { "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FF7900'" } } } } } } }]
}
```

### Secondary chart in grey (keeps orange rare)

A single-series chart takes `#FF7900` from the theme. When a page already has
two orange charts, add this inside the other charts' `"visual"` object:

```json
"objects": {
  "dataPoint": [{ "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#555555'" } } } } } } }]
}
```

### Visual titles

Each data visual gets a short title stating what it shows ("CA par région, en
MAD"): `pbi visual --no-sync set-container viz_1 --page <page> --title "…"`.

## Conditional formatting (tables and matrices only)

- **Target or good cells:** `pbi format background-conditional … --color "#FFF1E5"`.
  This uses the accent tint; the 8 px orange left border of the deck cannot be
  drawn in a cell, so state the target in the visual title.
- **Scales:** `pbi format background-gradient … --min-color "#FFFFFF" --max-color "#FF7900"`.
  This is the only gradient allowed.
- Red/green traffic lights are not part of the style. Use the accent tint for "good" and
  leave everything else neutral.

## Writing rules

- Headline = the finding, ≤ 12 words. Takeaway = the business implication, in one sentence.
- Translate technical metrics into plain language in the KPI captions ("5 churners sur 6", "1,7× meilleur que le hasard").
- One idea per page; 3–4 KPI tiles; 2–3 body visuals. Never add a page that only
  holds a table dump.
- Page order: synthesis (KPIs) → detail pages → recommendations. Page numbers start at `01`.

## Full build example

```bash
pbi report create . --name "ChurnDashboard" --dataset-path "../Churn.SemanticModel"
# write orange-dashboard-theme.json (above), then:
pbi report --no-sync set-theme --file orange-dashboard-theme.json
pbi report --no-sync add-page --display-name "Synthèse" --name synthese --width 1920 --height 1080
pbi report --no-sync set-background synthese --color "#EFEFEF"

V="pbi visual --no-sync"
$V add --page synthese --type textbox --name hdr_kicker   --x 64 --y 40 --width 1792 --height 40
$V add --page synthese --type textbox --name hdr_headline --x 64 --y 80 --width 1792 --height 64
for i in 1 2 3 4; do x=$((64 + (i-1)*454)); \
  $V add --page synthese --type card --name kpi_$i --x $x --y 168 --width 430 --height 152; done
$V add --page synthese --type bar  --name viz_1 --x 64  --y 344 --width 884 --height 572
$V add --page synthese --type line --name viz_2 --x 972 --y 344 --width 884 --height 572
$V add --page synthese --type shape   --name tk_bar    --x 64  --y 940  --width 1792 --height 72
$V add --page synthese --type shape   --name tk_stripe --x 64  --y 940  --width 12   --height 72
$V add --page synthese --type textbox --name tk_text   --x 100 --y 940  --width 1732 --height 72
$V add --page synthese --type textbox --name ftr_left  --x 64  --y 1028 --width 1180 --height 36
# cls_restricted ("Orange Restricted") was already added by add-page -- never touch it
$V add --page synthese --type textbox --name ftr_page  --x 1656 --y 1028 --width 200 --height 36

$V bind kpi_1 --page synthese --field "Churn[Recall]"
$V bind viz_1 --page synthese --category "Region[Name]" --value "Churn[Churners]"
$V set-container viz_1 --page synthese --title "Churners détectés par région"
# then: write the textbox/shape recipes into the decorative visual.json files,
# recolour max 2 hero tiles, and run:
pbi report validate
pbi report reload
```

## Checklist before reporting back

- [ ] Theme "Orange Dashboard" applied (`pbi report get-theme`); no other theme.
- [ ] Every page is 1920×1080 with an `#EFEFEF` background.
- [ ] Every page has a kicker, a conclusion headline, KPI row, body, takeaway bar, footer and page number.
- [ ] Every page shows the untouched **Orange Restricted** label in `#FF7900` (`pbi report validate` enforces it).
- [ ] At most 2 orange KPI values per row and at most 2 orange charts per page.
- [ ] Only approved visual types are used, and every data visual has a title.
- [ ] Every number in the text matches a `pbi dax execute` result; French formatting is used in French dashboards.
- [ ] `pbi report validate` passes, and the report opened in Desktop after `pbi report reload`.
