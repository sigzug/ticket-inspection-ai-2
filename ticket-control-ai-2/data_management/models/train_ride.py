from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field


class Station(Enum):
    OSLO_SENTRALSTATION = "Oslo S"
    OSLO_LUFTHAVN = "Oslo Lufthavn"
    EIDSVOLL_VERK = "Eidsvoll Verk"
    EIDSVOLL = "Eidsvoll"
    NATIONALTHEATERET = "Nationaltheatret"
    SKOYEN = "Skøyen"


class TrainRide(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    line: str
    departure_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    departure_station: Station
    arrival_station: Station
    occupied: bool
    ticket_inspection: bool
    checked_after_station: Station | None = Field(default=None)


ride_1 = TrainRide(
    line="R12",
    departure_time=datetime(2025, 12, 8, 15, 54, tzinfo=ZoneInfo('Europe/Oslo')),
    departure_station=Station.EIDSVOLL_VERK,
    arrival_station=Station.SKOYEN,
    occupied=True,
    ticket_inspection=False
)

