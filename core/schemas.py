from typing import Annotated

from pydantic import AwareDatetime, BaseModel, Field, PositiveInt


class ModelTimeInput(BaseModel):
    day: Annotated[int, Field(ge=1, le=31)]
    month: Annotated[int, Field(ge=1, le=12)]
    year: PositiveInt
    weekday: Annotated[int, Field(ge=0, le=6)]
    weekofyear: Annotated[int, Field(ge=1, le=52)]
    hour: Annotated[int, Field(ge=0, le=23)]
    minute: Annotated[int, Field(ge=0, le=59)]
    second: Annotated[int, Field(ge=0, le=59)]


class ModelInput(ModelTimeInput):
    # TODO add enums from models
    linje: str
    fra: str
    til: str
    fullt: bool


class UseModelRequest(BaseModel):
    # TODO add enums from models
    linje: str
    fra: str
    til: str
    fullt: bool
    departure_time: AwareDatetime


class UseModelResponse(BaseModel):
    checked: bool
