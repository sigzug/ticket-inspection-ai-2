from typing import Any
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
from pydantic import BaseModel, ValidationError


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: tuple = (500, 502, 503, 504),
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def _validate_response[T: BaseModel](
        self,
        response: requests.Response,
        model: type[T] | None = None
    ) -> T | None:
        if model is None:
            return None

        try:
            data = response.json()
            return model.model_validate(data)
        except ValidationError as e:
            raise ValueError(f"Response validation failed: {e}")
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON response: {e}")

    def get[T: BaseModel](
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        **kwargs
    ) -> T | None:
        url = self._build_url(endpoint)
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return self._validate_response(response, model)

    def post[T: BaseModel](
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        **kwargs
    ) -> T | None:
        url = self._build_url(endpoint)
        response = self.session.post(
            url,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return self._validate_response(response, model)

    def put[T: BaseModel](
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        **kwargs
    ) -> T | None:
        url = self._build_url(endpoint)
        response = self.session.put(
            url,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return self._validate_response(response, model)

    def patch[T: BaseModel](
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        **kwargs
    ) -> T | None:
        url = self._build_url(endpoint)
        response = self.session.patch(
            url,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return self._validate_response(response, model)

    def delete[T: BaseModel](
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        **kwargs
    ) -> T | None:
        url = self._build_url(endpoint)
        response = self.session.delete(
            url,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return self._validate_response(response, model)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
