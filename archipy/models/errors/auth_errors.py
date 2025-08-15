from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class UnauthenticatedError(BaseError):
    """Exception raised when a user is unauthenticated."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.UNAUTHENTICATED.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class InvalidCredentialsError(BaseError):
    """Exception raised for invalid credentials."""

    def __init__(
        self,
        username: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_CREDENTIALS.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"username": username} if username else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class TokenExpiredError(BaseError):
    """Exception raised when a token has expired."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.TOKEN_EXPIRED.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class InvalidTokenError(BaseError):
    """Exception raised when a token is invalid."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_TOKEN.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class SessionExpiredError(BaseError):
    """Exception raised when a session has expired."""

    def __init__(
        self,
        session_id: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.SESSION_EXPIRED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"session_id": session_id} if session_id else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class PermissionDeniedError(BaseError):
    """Exception raised when permission is denied."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.PERMISSION_DENIED.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class AccountLockedError(BaseError):
    """Exception raised when an account is locked."""

    def __init__(
        self,
        username: str | None = None,
        lockout_duration: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.ACCOUNT_LOCKED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if username:
            data["username"] = username
        if lockout_duration:
            data["lockout_duration"] = lockout_duration
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class AccountDisabledError(BaseError):
    """Exception raised when an account is disabled."""

    def __init__(
        self,
        username: str | None = None,
        reason: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.ACCOUNT_DISABLED.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if username:
            data["username"] = username
        if reason:
            data["reason"] = reason
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidVerificationCodeError(BaseError):
    """Exception raised when a verification code is invalid."""

    def __init__(
        self,
        code: str | None = None,
        remaining_attempts: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_VERIFICATION_CODE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if code:
            data["code"] = code
        if remaining_attempts is not None:
            data["remaining_attempts"] = remaining_attempts
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
