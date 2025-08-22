from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Line(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stations = models.ManyToManyField(Station, related_name="lines")

    def __str__(self):
        return self.name


class Stop(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="stops")
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name="stops")
    arrival_dt = models.DateTimeField()
    departure_dt = models.DateTimeField()

    def __str__(self):
        return f"{self.station.name} - {self.line.name} ({self.arrival_dt} to {self.departure_dt})"
