from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class DatabaseError(BaseError):
    """Base class for all database-related errors."""

    def __init__(
        self,
        database: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if database:
            data["database"] = database
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class DatabaseConnectionError(DatabaseError):
    """Exception raised for database connection errors."""

    def __init__(
        self,
        database: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_CONNECTION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(database, lang, error, additional_data)


class DatabaseQueryError(DatabaseError):
    """Exception raised for database query errors."""

    def __init__(
        self,
        database: str | None = None,
        query: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_QUERY_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if query:
            data["query"] = query
        if additional_data:
            data.update(additional_data)
        super().__init__(database, lang, error, data if data else None)


class DatabaseTransactionError(DatabaseError):
    """Exception raised for database transaction errors."""

    def __init__(
        self,
        database: str | None = None,
        transaction_id: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_TRANSACTION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if transaction_id:
            data["transaction_id"] = transaction_id
        if additional_data:
            data.update(additional_data)
        super().__init__(database, lang, error, data if data else None)


class DatabaseTimeoutError(DatabaseError):
    """Exception raised for database timeout errors."""

    def __init__(
        self,
        database: str | None = None,
        timeout: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_TIMEOUT_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if timeout:
            data["timeout"] = timeout
        if additional_data:
            data.update(additional_data)
        super().__init__(database, lang, error, data if data else None)


class DatabaseConstraintError(DatabaseError):
    """Exception raised for database constraint violations."""

    def __init__(
        self,
        database: str | None = None,
        constraint: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_CONSTRAINT_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if constraint:
            data["constraint"] = constraint
        if additional_data:
            data.update(additional_data)
        super().__init__(database, lang, error, data if data else None)


class DatabaseIntegrityError(DatabaseError):
    """Exception raised for database integrity violations."""

    def __init__(
        self,
        database: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_INTEGRITY_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(database, lang, error, additional_data)


class DatabaseDeadlockError(DatabaseError):
    """Exception raised for database deadlock errors."""

    def __init__(
        self,
        database: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_DEADLOCK_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(database, lang, error, additional_data)


class DatabaseSerializationError(DatabaseError):
    """Exception raised for database serialization errors."""

    def __init__(
        self,
        database: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_SERIALIZATION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(database, lang, error, additional_data)


class DatabaseConfigurationError(DatabaseError):
    """Exception raised for database configuration errors."""

    def __init__(
        self,
        database: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.DATABASE_CONFIGURATION_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(database, lang, error, additional_data)


class CacheError(BaseError):
    """Exception raised for cache access errors."""

    def __init__(
        self,
        cache_type: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.CACHE_ERROR.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if cache_type:
            data["cache_type"] = cache_type
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class CacheMissError(BaseError):
    """Exception raised when requested data is not found in cache."""

    def __init__(
        self,
        cache_key: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.CACHE_MISS.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"cache_key": cache_key} if cache_key else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
