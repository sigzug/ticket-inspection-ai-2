from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ComputeRequest(BaseModel):
    numbers: list[float] = Field(min_length=1)
    op: Literal["sum", "avg", "max", "min"]

    model_config = ConfigDict(str_strip_whitespace=True)


class ComputeResponse(BaseModel):
    operation: str
    count: int
    result: float
