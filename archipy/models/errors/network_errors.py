from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class NetworkError(BaseError):
    """Exception raised for network-related errors."""

    def __init__(
        self,
        service: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.NETWORK_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if service:
            data["service"] = service
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ConnectionTimeoutError(BaseError):
    """Exception raised when a connection times out."""

    def __init__(
        self,
        service: str | None = None,
        timeout: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.CONNECTION_TIMEOUT.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if service:
            data["service"] = service
        if timeout:
            data["timeout"] = timeout
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ServiceUnavailableError(BaseError):
    """Exception raised when a service is unavailable."""

    def __init__(
        self,
        service: str | None = None,
        retry_after: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.SERVICE_UNAVAILABLE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if service:
            data["service"] = service
        if retry_after:
            data["retry_after"] = retry_after
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class GatewayTimeoutError(BaseError):
    """Exception raised when a gateway times out."""

    def __init__(
        self,
        gateway: str | None = None,
        timeout: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.GATEWAY_TIMEOUT.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if gateway:
            data["gateway"] = gateway
        if timeout:
            data["timeout"] = timeout
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class BadGatewayError(BaseError):
    """Exception raised when a gateway returns an invalid response."""

    def __init__(
        self,
        gateway: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.BAD_GATEWAY.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if gateway:
            data["gateway"] = gateway
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class RateLimitExceededError(BaseError):
    """Exception raised when a rate limit is exceeded."""

    def __init__(
        self,
        rate_limit_type: str | None = None,
        retry_after: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.RATE_LIMIT_EXCEEDED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if rate_limit_type:
            data["rate_limit_type"] = rate_limit_type
        if retry_after:
            data["retry_after"] = retry_after
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
