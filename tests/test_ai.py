import json
from unittest.mock import patch

import pytest

from app.ai import DocumentationError, generate_workflow_documentation

VALID = json.dumps(
    {
        "overview": "Syncs new leads to the CRM.",
        "trigger": "A new row is added to the sheet.",
        "steps": ["Read the row", "Create the CRM contact"],
        "output": "A CRM contact.",
        "notes": "Runs every 5 minutes.",
    }
)


def _generate():
    return generate_workflow_documentation("Lead sync", "some text", "text")


def test_success_returns_markdown():
    with patch("app.ai._call_llm", return_value=VALID) as mock_call:
        result = _generate()
    assert "## Overview" in result
    assert "1. Read the row" in result
    assert mock_call.call_count == 1


def test_malformed_json_retries_once_then_succeeds():
    with patch("app.ai._call_llm", side_effect=["not json", VALID]) as mock_call:
        result = _generate()
    assert "## Steps" in result
    assert mock_call.call_count == 2


def test_invalid_output_twice_raises_clean_error():
    bad = ["not json", '{"overview": "missing other fields"}']
    with patch("app.ai._call_llm", side_effect=bad) as mock_call:
        with pytest.raises(DocumentationError):
            _generate()
    assert mock_call.call_count == 2


def test_timeout_raises_clean_error_without_retry():
    with patch("app.ai._call_llm", side_effect=TimeoutError("timed out")) as mock_call:
        with pytest.raises(DocumentationError) as exc:
            _generate()
    assert "timed out" not in str(exc.value)
    assert mock_call.call_count == 1