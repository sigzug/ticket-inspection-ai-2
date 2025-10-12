from typing import Annotated, Any

from pydantic import AwareDatetime, BaseModel, Field, PositiveInt, field_validator


class ModelTimeInput(BaseModel):
    day: Annotated[int, Field(ge=1, le=31)]
    month: Annotated[int, Field(ge=1, le=12)]
    year: PositiveInt
    weekday: Annotated[int, Field(ge=0, le=6)]
    weekofyear: Annotated[int, Field(ge=1, le=52)]
    hour: Annotated[int, Field(ge=0, le=23)]
    minute: Annotated[int, Field(ge=0, le=59)]


class ModelInput(ModelTimeInput):
    # TODO add enums from models
    line: int
    departure_station: int
    arrival_station: int
    only_standing: int

    @field_validator("line", "departure_station", "arrival_station", mode="before")
    @classmethod
    def to_lowercase(cls, v: Any) -> str:
        if isinstance(v, str):
            return v.lower()
        return v


class UseModelRequest(BaseModel):
    # TODO add enums from models
    line: str
    departure_station: str
    arrival_station: str
    only_standing: bool
    departure_time: AwareDatetime

    @field_validator("line", "departure_station", "arrival_station", mode="before")
    @classmethod
    def to_lowercase(cls, v: Any) -> str:
        if isinstance(v, str):
            return v.lower()
        return v


class UseModelResponse(BaseModel):
    checked: bool
