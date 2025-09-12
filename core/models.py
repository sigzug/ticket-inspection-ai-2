

# class Station(Model):
#     name = CharField(max_length=100)
#
#
# class Line(Model):
#     name = CharField(max_length=100)
#
#
# class Ride(Model):
#     line = ForeignKey(Line, on_delete=SET_NULL)
#     datetime = DateTimeField()
#     departure_station = ForeignKey(Station, on_delete=SET_NULL)
#     arrival_station = ForeignKey(Station, on_delete=SET_NULL)
#     full = BooleanField(default=False)
#
#     checked = BooleanField(default=False)
#     checked_after = ForeignKey(Station, on_delete=SET_NULL)
