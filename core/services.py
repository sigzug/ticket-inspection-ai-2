import os
from datetime import datetime

import xgboost as xgb
from django.http import Http404

from config.settings import BASE_DIR
from core.schemas import ModelInput, ModelTimeInput, UseModelRequest, UseModelResponse


def get_newest_model() -> xgb.XGBClassifier | None:
    model_dir = BASE_DIR / "models"
    files = [f for f in model_dir.iterdir() if f.is_file()]
    if not files:
        return None
    newest_file_path = max(files, key=os.path.getmtime)

    model = xgb.XGBClassifier()
    model.load_model(newest_file_path)
    return model


def create_time_date_input(departure_time: datetime) -> ModelTimeInput:
    return ModelTimeInput(
        day=departure_time.day,
        month=departure_time.month,
        year=departure_time.year,
        weekday=departure_time.weekday(),
        weekofyear=departure_time.isocalendar().week,
        hour=departure_time.hour,
        minute=departure_time.minute,
        second=departure_time.second,
    )


def run_model(input_data: UseModelRequest) -> UseModelResponse:
    model = get_newest_model()
    if model is None:
        raise Http404("Found no models.")

    model_time_input = create_time_date_input(input_data.departure_time)

    input_data_dict = input_data.model_dump()
    input_data_dict.pop("departure_time")
    input_data_dict.update(model_time_input.model_dump())
    model_input = ModelInput(**input_data_dict)

    # Convert string to categorical

    preds = model.predict(model_input.model_dump())
    return UseModelResponse(checked=preds)
