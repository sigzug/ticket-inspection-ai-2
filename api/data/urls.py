def get_vy_data()

def update_stations():
    from data.models import Station

    # Example data to update or create stations
    stations_data = [
        {"name": "Station A"},
        {"name": "Station B"},
        {"name": "Station C"},
    ]

    for station_data in stations_data:
        Station.objects.update_or_create(
            name=station_data["name"],
            defaults=station_data,
        )

def update_lines():