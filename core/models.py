from django.db import models
from django.db.models import SET_NULL, Q


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Line(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Ride(models.Model):
    line = models.ForeignKey(Line, on_delete=SET_NULL, null=True, blank=True, related_name="rides")
    departure_time = models.DateTimeField(db_index=True)
    departure_station = models.ForeignKey(
        Station, on_delete=SET_NULL, null=True, blank=True, related_name="rides_departing"
    )
    arrival_station = models.ForeignKey(
        Station, on_delete=SET_NULL, null=True, blank=True, related_name="rides_arriving"
    )
    only_standing = models.BooleanField(default=False, db_index=True)

    checked = models.BooleanField(default=False, db_index=True)
    checked_after = models.ForeignKey(
        Station, on_delete=SET_NULL, null=True, blank=True, related_name="rides_checked_after"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(departure_station=models.F("arrival_station")),
                name="ride_departure_ne_arrival",
            ),
        ]
        indexes = [
            models.Index(fields=["line", "departure_time"]),
        ]

    def __str__(self) -> str:
        return f"{self.line} {self.departure_time:%Y-%m-%d %H:%M}"
