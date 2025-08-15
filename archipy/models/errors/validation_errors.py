from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class InvalidArgumentError(BaseError):
    """Exception raised for invalid arguments."""

    def __init__(
        self,
        argument_name: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_ARGUMENT.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"argument": argument_name} if argument_name else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidFormatError(BaseError):
    """Exception raised for invalid data formats."""

    def __init__(
        self,
        format_type: str | None = None,
        expected_format: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_FORMAT.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if format_type:
            data["format_type"] = format_type
        if expected_format:
            data["expected_format"] = expected_format
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidEmailError(BaseError):
    """Exception raised for invalid email formats."""

    def __init__(
        self,
        email: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_EMAIL.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"email": email} if email else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidPhoneNumberError(BaseError):
    """Exception raised for invalid phone numbers."""

    def __init__(
        self,
        phone_number: str,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_PHONE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"phone_number": phone_number}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data)


class InvalidLandlineNumberError(BaseError):
    """Exception raised for invalid landline numbers."""

    def __init__(
        self,
        landline_number: str,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_LANDLINE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"landline_number": landline_number}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data)


class InvalidNationalCodeError(BaseError):
    """Exception raised for invalid national codes."""

    def __init__(
        self,
        national_code: str,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_NATIONAL_CODE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"national_code": national_code}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data)


class InvalidPasswordError(BaseError):
    """Exception raised when a password does not meet the security requirements."""

    def __init__(
        self,
        requirements: list[str] | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_PASSWORD.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"requirements": requirements} if requirements else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidDateError(BaseError):
    """Exception raised for invalid date formats."""

    def __init__(
        self,
        date: str | None = None,
        expected_format: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_DATE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if date:
            data["date"] = date
        if expected_format:
            data["expected_format"] = expected_format
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidUrlError(BaseError):
    """Exception raised for invalid URL formats."""

    def __init__(
        self,
        url: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_URL.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"url": url} if url else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidIpError(BaseError):
    """Exception raised for invalid IP address formats."""

    def __init__(
        self,
        ip: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_IP.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"ip": ip} if ip else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidJsonError(BaseError):
    """Exception raised for invalid JSON formats."""

    def __init__(
        self,
        json_data: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_JSON.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if json_data:
            data["json_data"] = json_data
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidTimestampError(BaseError):
    """Exception raised when a timestamp format is invalid."""

    def __init__(
        self,
        timestamp: str | None = None,
        expected_format: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_TIMESTAMP.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if timestamp:
            data["timestamp"] = timestamp
        if expected_format:
            data["expected_format"] = expected_format
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class OutOfRangeError(BaseError):
    """Exception raised when a value is out of range."""

    def __init__(
        self,
        field_name: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.OUT_OF_RANGE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"field": field_name} if field_name else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
