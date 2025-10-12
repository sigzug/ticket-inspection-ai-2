import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import xgboost as xgb
from django.http import Http404

from config.settings import BASE_DIR
from core.schemas import ModelTimeInput, UseModelRequest, UseModelResponse


def _get_newest_dir() -> Path:
    model_dir = BASE_DIR / "models"

    # List all directories with datetime names
    dirs = [d for d in model_dir.iterdir() if d.is_dir()]
    if not dirs:
        return None

    # Find the newest directory by modification time
    return max(dirs, key=os.path.getmtime)


def get_newest_model() -> xgb.XGBClassifier | None:
    newest_dir = _get_newest_dir()

    # Find the model file inside the newest directory
    model_files = list(newest_dir.glob("*.pkl"))
    if not model_files:
        return None
    model_file = model_files[0]
    model = xgb.XGBClassifier()
    model.load_model(model_file)
    return model


def get_all_categories() -> dict[str, pd.Categorical]:
    """Get all categorical objects from the newest model's categories directory."""
    newest_dir = _get_newest_dir()

    # Look for categories directory
    categories_dir = newest_dir / "categories"
    if not categories_dir.exists():
        return []

    # Get all pickle files in categories directory
    category_files = list(categories_dir.glob("*.pkl"))

    # Load in the categorical objects
    categories = {}
    for cat_file in category_files:
        with open(cat_file, "rb") as f:
            category = pickle.load(f)
            categories[cat_file.stem] = category
    return categories


def expected_feature_order(model) -> list[str]:
    booster = getattr(model, "get_booster", None)
    if booster is not None:
        names = getattr(booster, "feature_names", None)
        if names:
            return list(names)

    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    raise RuntimeError("Finner ikke forventet feature-rekkefølge i modellen.")

def align_row_to_model(data: Mapping[str, Any], model) -> pd.DataFrame:
    expected = expected_feature_order(model)

    missing = [k for k in expected if k not in data]
    if missing:
        raise KeyError(f"Mangler features i input: {missing}")

    row = [data[k] for k in expected]
    return pd.DataFrame([row], columns=expected)


def create_time_date_input(departure_time: datetime) -> ModelTimeInput:
    return ModelTimeInput(
        day=departure_time.day,
        month=departure_time.month,
        year=departure_time.year,
        weekday=departure_time.weekday(),
        weekofyear=departure_time.isocalendar().week,
        hour=departure_time.hour,
        minute=departure_time.minute,
    )


def run_model(input_data: UseModelRequest) -> UseModelResponse:
    model = get_newest_model()
    if model is None:
        raise Http404("Found no models.")

    model_time_input = create_time_date_input(input_data.departure_time)

    d = input_data.model_dump()
    d.pop("departure_time")
    d.update(model_time_input.model_dump())

    all_categories = get_all_categories()
    for field in ["line", "departure_station", "arrival_station"]:
        if field in all_categories:
            cat = all_categories[field]
            try:
                d[field] = cat.categories.get_loc(d[field])
            except KeyError:
                d[field] = -1
        else:
            d[field] = -1

    d["only_standing"] = int(d["only_standing"])

    x = align_row_to_model(d, model)
    preds = model.predict(x)  # evt. model.predict(x.to_numpy()) hvis du vil hoppe over navnesjekk
    return UseModelResponse(checked=preds)
