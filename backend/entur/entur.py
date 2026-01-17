import re
import io
import xml.etree.ElementTree as ET
import zipfile
from typing import Any

import requests

from backend.clients import BaseAPIClient
from backend.entur.models import Codespace, StopPlacesResponse


class EnturClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url="https://api.entur.io")

    def get_stop_places(
        self, params: dict[str, Any] | None = None, **kwargs
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
            **kwargs,
        )


def _convert_to_xml_element(data: Any) -> ET.Element:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        xml_names = [n for n in zf.namelist() if n.lower().endswith(".xml")]
        if not xml_names:
            raise ValueError("No .xml files found in the ZIP")

        xml_bytes = zf.read(xml_names[0])
    return ET.fromstring(xml_bytes)


def get_timetable_data(codespace: Codespace):
    url = f"https://storage.googleapis.com/marduk-production/outbound/netex/rb_{codespace.value}-aggregated-netex.zip"
    response = requests.get(url)
    response.raise_for_status()

    root = _convert_to_xml_element(response.content)
    ns = {"n": "http://www.netex.org.uk/netex"}

    return root


if __name__ == "__main__":
    print(get_timetable_data(Codespace.VYG))
