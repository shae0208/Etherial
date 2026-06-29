import json
from pathlib import Path
from typing import Any, Dict, List


class SubmitService:
    @staticmethod
    def get_submission_path(storage_path: str | Path | None = None) -> Path:
        if storage_path is not None:
            return Path(storage_path)

        return Path(__file__).resolve().parent.parent / "data" / "submissions.json"

    @staticmethod
    def load_submissions(storage_path: str | Path | None = None) -> List[Dict[str, Any]]:
        path = SubmitService.get_submission_path(storage_path)
        if not path.exists():
            return []

        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        return data if isinstance(data, list) else []

    @staticmethod
    def add_submission(submission: Dict[str, Any], storage_path: str | Path | None = None) -> Dict[str, Any]:
        path = SubmitService.get_submission_path(storage_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        submissions = SubmitService.load_submissions(storage_path=path)
        payload = {
            "animus": submission.get("animus", "").strip(),
            "path": submission.get("path", "").strip(),
            "value": submission.get("value", "").strip(),
            "reason": submission.get("reason", "").strip(),
            "submitted_by": submission.get("submitted_by", "Unknown").strip() or "Unknown",
        }

        submissions.append(payload)

        with path.open("w", encoding="utf-8") as handle:
            json.dump(submissions, handle, indent=2)
            handle.write("\n")

        return {"status": "queued", "submission": payload}
