import pandas as pd

from backend.server.settings import ROOT_PATH
import pickle as pkl
from pathlib import Path

from datetime import datetime


AI_FOLDER_PATH = Path(ROOT_PATH / "ai" / "models")


def _parse_iso_dt(name: str) -> datetime:
    """
    Parse an ISO-8601 string into a datetime.
    Supports 'Z' (UTC) suffix and allows a space instead of 'T'.
    """
    s = name.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    if " " in s and "T" not in s:
        s = s.replace(" ", "T")
    return datetime.fromisoformat(s)


def _get_newest_model_folder() -> Path:
    """
    Return the newest model folder based on the folder name,
    where each subfolder name is an ISO datetime string.
    """
    candidates = []
    for f in AI_FOLDER_PATH.iterdir():
        if not f.is_dir():
            continue
        try:
            ts = _parse_iso_dt(f.name)
        except Exception:
            # Skip folders that are not valid ISO timestamps
            continue
        candidates.append((ts, f))

    if not candidates:
        raise FileNotFoundError(f"No ISO-named model folders found in {AI_FOLDER_PATH}")

    # Pick the folder with the latest timestamp
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def load_in_model_categories() -> dict[str, pd.Categorical]:
    """
    Load pickled pandas Categorical objects from the newest model's 'categories' folder.
    Returns a dict keyed by the last path component (file name without extension).
    """
    newest_model_folder = _get_newest_model_folder()
    categories_folder = newest_model_folder / "categories"

    if not categories_folder.exists() or not categories_folder.is_dir():
        raise FileNotFoundError(f"Categories folder not found: {categories_folder}")

    categories: dict[str, pd.Categorical] = {}
    for item in categories_folder.iterdir():
        if not item.is_file():
            continue
        key = item.stem
        with open(item, "rb") as f:
            categories[key] = pkl.load(f)
    return categories


if __name__ == "__main__":
    print(load_in_model_categories())
