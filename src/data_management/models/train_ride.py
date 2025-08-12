from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, create_engine
from sqlmodel import SQLModel, Field, select

from src.data_management.setup_db import create_db_and_tables, get_session


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
    checked_after_station: Station | None = Field(default=None)


def test() -> None:
    """Test function to create a TrainRide instance."""

    create_db_and_tables()

    ride_1 = TrainRide(
        line="R12",
        departure_time=datetime(2025, 12, 8, 15, 54, tzinfo=ZoneInfo("Europe/Oslo")),
        departure_station=Station.EIDSVOLL_VERK,
        arrival_station=Station.SKOYEN,
        occupied=True,
        ticket_inspection=False,
    )

    with get_session() as s:
        s.add(ride_1)
        s.commit()
        s.refresh(ride_1)

        stmt = select(TrainRide).where(TrainRide.line == "R12")
        rows = s.exec(stmt).all()
        return rows


if __name__ == "__main__":
    print(test())
    