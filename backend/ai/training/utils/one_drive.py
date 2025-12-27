from pathlib import Path

import msal
import requests

MS_APPLICATION_ID = "ea99bfa2-4b72-444b-b68a-37876b79917c"
AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["User.Read", "Files.Read"]
GRAPH = "https://graph.microsoft.com/v1.0"
CACHE_PATH = Path("../.msal_cache.json")


class OneDriveAuth:
    _instance: "OneDriveAuth | None" = None

    def __new__(cls) -> "OneDriveAuth":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self._cache = msal.SerializableTokenCache()
        if CACHE_PATH.exists():
            self._cache.deserialize(CACHE_PATH.read_text(encoding="utf-8"))

        self._app = msal.PublicClientApplication(
            client_id=MS_APPLICATION_ID,
            authority=AUTHORITY,
            token_cache=self._cache,
        )

    def _save_cache(self) -> None:
        if self._cache.has_state_changed:
            CACHE_PATH.write_text(self._cache.serialize(), encoding="utf-8")

    def get_token(self) -> str:
        accounts = self._app.get_accounts()
        result = self._app.acquire_token_silent(
            SCOPES,
            account=accounts[0] if accounts else None,
        )

        if not result:
            flow = self._app.initiate_device_flow(scopes=SCOPES)
            if "user_code" not in flow:
                raise RuntimeError(f"Device flow failed: {flow}")

            print(flow["message"])
            result = self._app.acquire_token_by_device_flow(flow)

        self._save_cache()

        token = result.get("access_token")
        if not token:
            raise RuntimeError(f"Token error: {result}")

        return token


class OneDriveClient:
    def __init__(self, auth: OneDriveAuth) -> None:
        self._auth = auth

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._auth.get_token()}",
        }

    def get_file_bytes(self, onedrive_path: str) -> bytes:
        """
        Download a file from OneDrive and return its full content as bytes.

        Example:
            data = client.get_file_bytes("Documents/report.xlsx")
        """
        url = f"{GRAPH}/me/drive/root:/{onedrive_path}:/content"

        r = requests.get(
            url,
            headers=self._headers(),
            timeout=60,
        )
        r.raise_for_status()
        return r.content
