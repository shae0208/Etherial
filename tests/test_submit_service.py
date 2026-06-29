import json

from services.submit_service import SubmitService


def test_add_submission_writes_expected_payload(tmp_path):
    storage_path = tmp_path / "submissions.json"
    submission = {
        "animus": "airon",
        "path": "build.shells",
        "value": "['Lighthouse']",
        "reason": "Needs a more up-to-date shell recommendation.",
        "submitted_by": "Test User",
    }

    result = SubmitService.add_submission(submission, storage_path=storage_path)

    assert result["status"] == "queued"
    saved = json.loads(storage_path.read_text(encoding="utf-8"))
    assert len(saved) == 1
    assert saved[0]["animus"] == "airon"
    assert saved[0]["path"] == "build.shells"
    assert saved[0]["value"] == "['Lighthouse']"
