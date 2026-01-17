from typing import Any
from backend.clients import BaseAPIClient
from backend.entur.models import StopPlacesResponse


class EnturClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url="https://api.entur.io")

    def get_stop_places(
            self,
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> StopPlacesResponse | None:
        """
        Get stop places from Entur API.

        Args:
            params: Query parameters for filtering stop places
            **kwargs: Additional arguments to pass to requests

        Returns:
            StopPlacesResponse containing a list of StopPlace objects
        """
        return self.get(
            endpoint="/stop-places/v1/read/stop-places",
            params=params,
            model=StopPlacesResponse,
            **kwargs
        )


if __name__ == "__main__":
    client = EnturClient()
    print(client.get_stop_places().model_dump_json(indent=2))
