from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class InternalError(BaseError):
    """Exception raised for unexpected internal errors."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INTERNAL_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class UnknownError(BaseError):
    """Exception raised for unknown or unexpected error conditions."""

    def __init__(
        self,
        error_code: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.UNKNOWN_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if error_code:
            data["error_code"] = error_code
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class AbortedError(BaseError):
    """Exception raised when an operation is aborted."""

    def __init__(
        self,
        operation: str | None = None,
        reason: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.ABORTED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if operation:
            data["operation"] = operation
        if reason:
            data["reason"] = reason
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class DeadlockDetectedError(BaseError):
    """Exception raised when a deadlock is detected in the system."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DEADLOCK.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if resource_type:
            data["resource_type"] = resource_type
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ConfigurationError(BaseError):
    """Exception raised for system configuration errors."""

    def __init__(
        self,
        config_key: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.CONFIGURATION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if config_key:
            data["config_key"] = config_key
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class UnavailableError(BaseError):
    """Exception raised when a requested service or feature is unavailable."""

    def __init__(
        self,
        service: str | None = None,
        reason: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.UNAVAILABLE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if service:
            data["service"] = service
        if reason:
            data["reason"] = reason
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
