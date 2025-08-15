from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class NotFoundError(BaseError):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.NOT_FOUND.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"resource_type": resource_type} if resource_type else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class AlreadyExistsError(BaseError):
    """Exception raised when a resource already exists."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.ALREADY_EXISTS.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"resource_type": resource_type} if resource_type else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ConflictError(BaseError):
    """Exception raised when there is a resource conflict."""

    def __init__(
        self,
        resource_type: str | None = None,
        resource_id: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.CONFLICT.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if resource_type:
            data["resource_type"] = resource_type
        if resource_id:
            data["resource_id"] = resource_id
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ResourceLockedError(BaseError):
    """Exception raised when a resource is locked."""

    def __init__(
        self,
        resource_id: str | None = None,
        lock_owner: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.RESOURCE_LOCKED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if resource_id:
            data["resource_id"] = resource_id
        if lock_owner:
            data["lock_owner"] = lock_owner
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ResourceBusyError(BaseError):
    """Exception raised when a resource is busy."""

    def __init__(
        self,
        resource_id: str | None = None,
        busy_reason: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.RESOURCE_BUSY.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if resource_id:
            data["resource_id"] = resource_id
        if busy_reason:
            data["busy_reason"] = busy_reason
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class DataLossError(BaseError):
    """Exception raised when data is lost."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATA_LOSS.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class InvalidEntityTypeError(BaseError):
    """Exception raised for invalid entity types."""

    def __init__(
        self,
        message: str | None = None,
        expected_type: str | None = None,
        actual_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_ENTITY_TYPE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if message:
            data["message"] = message
        if expected_type:
            data["expected_type"] = expected_type
        if actual_type:
            data["actual_type"] = actual_type
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class FileTooLargeError(BaseError):
    """Exception raised when a file is too large."""

    def __init__(
        self,
        file_name: str | None = None,
        file_size: int | None = None,
        max_size: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.FILE_TOO_LARGE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if file_name:
            data["file_name"] = file_name
        if file_size:
            data["file_size"] = file_size
        if max_size:
            data["max_size"] = max_size
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidFileTypeError(BaseError):
    """Exception raised for invalid file types."""

    def __init__(
        self,
        file_name: str | None = None,
        file_type: str | None = None,
        allowed_types: list[str] | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_FILE_TYPE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if file_name:
            data["file_name"] = file_name
        if file_type:
            data["file_type"] = file_type
        if allowed_types:
            data["allowed_types"] = allowed_types
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class QuotaExceededError(BaseError):
    """Exception raised when a quota is exceeded."""

    def __init__(
        self,
        quota_type: str | None = None,
        current_usage: int | None = None,
        quota_limit: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.QUOTA_EXCEEDED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if quota_type:
            data["quota_type"] = quota_type
        if current_usage:
            data["current_usage"] = current_usage
        if quota_limit:
            data["quota_limit"] = quota_limit
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class ResourceExhaustedError(BaseError):
    """Exception raised when a resource is exhausted."""

    def __init__(
        self,
        resource_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.RESOURCE_EXHAUSTED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"resource_type": resource_type} if resource_type else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class StorageError(BaseError):
    """Exception raised for storage-related errors."""

    def __init__(
        self,
        storage_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.STORAGE_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"storage_type": storage_type} if storage_type else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
