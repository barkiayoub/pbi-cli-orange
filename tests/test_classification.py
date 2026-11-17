"""Tests for the mandatory, read-only 'Orange Restricted' classification label."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pbi_cli.core.bulk_backend import visual_bulk_delete, visual_bulk_update
from pbi_cli.core.classification import (
    LABEL_COLOR,
    LABEL_TEXT,
    LABEL_VISUAL_NAME,
    check_page_label,
)
from pbi_cli.core.errors import PbiCliError
from pbi_cli.core.format_backend import format_clear
from pbi_cli.core.pbir_validators import validate_report_full
from pbi_cli.core.report_backend import (
    apply_classification,
    page_add,
    report_create,
    report_validate,
)
from pbi_cli.core.visual_backend import (
    visual_add,
    visual_delete,
    visual_list,
    visual_set_container,
    visual_update,
)


@pytest.fixture
def definition(tmp_path: Path) -> Path:
    result = report_create(tmp_path, "Dash")
    defn = Path(result["definition_path"])
    page_add(defn, "Synthèse", name="synthese", width=1920, height=1080)
    return defn


def _label_file(defn: Path, page: str = "synthese") -> Path:
    return defn / "pages" / page / "visuals" / LABEL_VISUAL_NAME / "visual.json"


def test_add_page_inserts_label(definition: Path) -> None:
    data = json.loads(_label_file(definition).read_text(encoding="utf-8"))
    run = data["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
    assert run["value"] == LABEL_TEXT
    assert run["textStyle"]["color"] == LABEL_COLOR
    assert data["position"]["x"] == 1268
    assert data["position"]["y"] == 1028


def test_label_stays_on_top_and_outside_auto_layout(definition: Path) -> None:
    # auto-placement on a fresh page ignores the footer label (starts at the top)
    auto = visual_add(definition, "synthese", "card", name="kpi_1")
    assert auto["y"] == 70
    # a full-bleed footer band added later must still sit below the label
    band = visual_add(
        definition, "synthese", "shape", name="ftr_band", x=0, y=1008, width=1920, height=72
    )
    label = json.loads(_label_file(definition).read_text(encoding="utf-8"))
    for name in (band["name"], auto["name"]):
        vfile = definition / "pages" / "synthese" / "visuals" / name / "visual.json"
        z = json.loads(vfile.read_text(encoding="utf-8"))["position"]["z"]
        assert z < label["position"]["z"]


def test_new_report_page_validates(definition: Path) -> None:
    assert report_validate(definition)["valid"] is True
    assert validate_report_full(definition)["valid"] is True


@pytest.mark.parametrize(
    "call",
    [
        lambda d: visual_update(d, "synthese", LABEL_VISUAL_NAME, x=0),
        lambda d: visual_update(d, "synthese", LABEL_VISUAL_NAME, hidden=True),
        lambda d: visual_delete(d, "synthese", LABEL_VISUAL_NAME),
        lambda d: visual_set_container(d, "synthese", LABEL_VISUAL_NAME, title="x"),
        lambda d: visual_add(d, "synthese", "textbox", name=LABEL_VISUAL_NAME),
        lambda d: format_clear(d, "synthese", LABEL_VISUAL_NAME),
    ],
)
def test_cli_writes_to_label_are_refused(definition: Path, call) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(PbiCliError, match="cannot be added, modified"):
        call(definition)
    assert check_page_label(definition / "pages" / "synthese") == []


def test_bulk_operations_skip_label(definition: Path) -> None:
    visual_add(definition, "synthese", "textbox", name="hdr_kicker")
    visual_bulk_update(definition, "synthese", where_type="textbox", set_hidden=True)
    visual_bulk_delete(definition, "synthese", where_type="textbox")
    names = [v["name"] for v in visual_list(definition, "synthese")]
    assert names == [LABEL_VISUAL_NAME]
    assert check_page_label(definition / "pages" / "synthese") == []


def test_validate_fails_when_label_missing_or_altered(definition: Path) -> None:
    label = _label_file(definition)
    data = json.loads(label.read_text(encoding="utf-8"))
    run = data["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
    run["value"] = "Orange Public"
    run["textStyle"]["color"] = "#111111"
    label.write_text(json.dumps(data), encoding="utf-8")

    result = report_validate(definition)
    assert result["valid"] is False
    assert any("Orange Restricted" in e for e in result["errors"])

    label.unlink()
    assert validate_report_full(definition)["valid"] is False


def test_apply_classification_restores_label(definition: Path) -> None:
    _label_file(definition).unlink()
    result = apply_classification(definition)
    assert result["pages"] == [{"page": "synthese", "action": "restored"}]
    assert report_validate(definition)["valid"] is True
