"""Mandatory, read-only "Orange Restricted" classification label.

Every page of every dashboard carries a textbox visual named
``cls_restricted`` that reads ``Orange Restricted`` in Orange ``#FF7900``.
The label is written by pbi-cli itself (on ``add-page`` and by
``report apply-classification``) and every CLI write path refuses to touch it.
``report validate`` fails when a page is missing the label or the label has
been altered by hand.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pbi_cli.core.errors import PbiCliError

LABEL_VISUAL_NAME = "cls_restricted"
LABEL_TEXT = "Orange Restricted"
LABEL_COLOR = "#FF7900"
LABEL_FONT_SIZE = "12pt"

# Footer slot on the Orange grid: between the footer text and the page number.
# Offsets are taken from the bottom-right corner so the label also lands in the
# footer on pages that are not 1920x1080 (1920x1080 -> x=1268, y=1028).
_LABEL_WIDTH = 364
_LABEL_HEIGHT = 36
_RIGHT_OFFSET = 652  # 64 margin + 200 page number + 24 gap + 364 label
_BOTTOM_OFFSET = 52

# z-order high enough to sit above every other visual on the page.
_LABEL_Z = 100000

_VISUAL_CONTAINER_SCHEMA = (
    "https://developer.microsoft.com/json-schemas/"
    "fabric/item/report/definition/visualContainer/2.7.0/schema.json"
)


def is_protected(visual_name: str | None) -> bool:
    """Return True if the visual is the protected classification label."""
    return visual_name == LABEL_VISUAL_NAME


def ensure_not_protected(visual_name: str | None) -> None:
    """Raise if a write targets the protected classification label."""
    if is_protected(visual_name):
        raise PbiCliError(
            f"'{LABEL_VISUAL_NAME}' is the mandatory '{LABEL_TEXT}' classification "
            "label. It cannot be added, modified, moved, hidden or deleted. "
            "Use 'pbi report apply-classification' to restore it."
        )


def build_label_visual(page_width: int, page_height: int) -> dict[str, Any]:
    """Return the canonical visual.json content for the classification label."""
    x = max(page_width - _RIGHT_OFFSET, 0)
    y = max(page_height - _BOTTOM_OFFSET, 0)
    return {
        "$schema": _VISUAL_CONTAINER_SCHEMA,
        "name": LABEL_VISUAL_NAME,
        "position": {
            "x": x,
            "y": y,
            "z": _LABEL_Z,
            "height": _LABEL_HEIGHT,
            "width": _LABEL_WIDTH,
            "tabOrder": _LABEL_Z,
        },
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [
                                        {
                                            "value": LABEL_TEXT,
                                            "textStyle": {
                                                "fontFamily": "Arial",
                                                "fontSize": LABEL_FONT_SIZE,
                                                "fontWeight": "bold",
                                                "color": LABEL_COLOR,
                                            },
                                        }
                                    ],
                                    "horizontalTextAlignment": "right",
                                }
                            ]
                        }
                    }
                ]
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
            },
            "drillFilterOtherVisuals": True,
        },
    }


def write_label(page_dir: Path) -> dict[str, Any]:
    """(Re)write the canonical label into a page folder. Returns a status dict."""
    page_json = page_dir / "page.json"
    if not page_json.exists():
        raise PbiCliError(f"Page '{page_dir.name}' not found.")
    page_data = json.loads(page_json.read_text(encoding="utf-8"))
    width = int(page_data.get("width", 1280))
    height = int(page_data.get("height", 720))

    label_dir = page_dir / "visuals" / LABEL_VISUAL_NAME
    label_dir.mkdir(parents=True, exist_ok=True)
    label_file = label_dir / "visual.json"
    expected = build_label_visual(width, height)

    previous_errors = check_page_label(page_dir)
    label_file.write_text(
        json.dumps(expected, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return {
        "page": page_dir.name,
        "action": "restored" if previous_errors else "unchanged",
    }


def check_page_label(page_dir: Path) -> list[str]:
    """Return a list of problems with the page's classification label (empty = OK)."""
    label_file = page_dir / "visuals" / LABEL_VISUAL_NAME / "visual.json"
    if not label_file.exists():
        return [f"Missing mandatory '{LABEL_TEXT}' label ({LABEL_VISUAL_NAME})"]

    try:
        data = json.loads(label_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [f"'{LABEL_TEXT}' label is not valid JSON"]

    problems: list[str] = []
    visual = data.get("visual", {})
    if visual.get("visualType") != "textbox":
        problems.append(f"'{LABEL_TEXT}' label must be a textbox")
    if data.get("isHidden"):
        problems.append(f"'{LABEL_TEXT}' label must not be hidden")

    runs = _text_runs(visual)
    text = "".join(str(r.get("value", "")) for r in runs)
    if text != LABEL_TEXT:
        problems.append(f"Label text must be exactly '{LABEL_TEXT}' (found '{text}')")
    for run in runs:
        color = str(run.get("textStyle", {}).get("color", "")).upper()
        if color != LABEL_COLOR:
            problems.append(f"Label colour must be {LABEL_COLOR} (found '{color or 'none'}')")
            break

    pos = data.get("position", {})
    if pos.get("width", 0) <= 0 or pos.get("height", 0) <= 0:
        problems.append("Label has no visible size")
    return problems


def _text_runs(visual: dict[str, Any]) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for general in visual.get("objects", {}).get("general", []):
        for paragraph in general.get("properties", {}).get("paragraphs", []):
            runs.extend(paragraph.get("textRuns", []))
    return runs
