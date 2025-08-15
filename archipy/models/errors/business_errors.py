from archipy.models.dtos.error_dto import ErrorDetailDTO
from archipy.models.errors.base_error import BaseError
from archipy.models.types.error_message_types import ErrorMessageType
from archipy.models.types.language_type import LanguageType


class InvalidStateError(BaseError):
    """Exception raised when an operation is attempted in an invalid state."""

    def __init__(
        self,
        current_state: str | None = None,
        expected_state: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_STATE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if current_state:
            data["current_state"] = current_state
        if expected_state:
            data["expected_state"] = expected_state
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class FailedPreconditionError(BaseError):
    """Exception raised when a precondition for an operation is not met."""

    def __init__(
        self,
        precondition: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.FAILED_PRECONDITION.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if precondition:
            data["precondition"] = precondition
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class BusinessRuleViolationError(BaseError):
    """Exception raised when a business rule is violated."""

    def __init__(
        self,
        rule: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.BUSINESS_RULE_VIOLATION.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if rule:
            data["rule"] = rule
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InvalidOperationError(BaseError):
    """Exception raised when an operation is not allowed in the current context."""

    def __init__(
        self,
        operation: str | None = None,
        context: str | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INVALID_OPERATION.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {}
        if operation:
            data["operation"] = operation
        if context:
            data["context"] = context
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)


class InsufficientFundsError(BaseError):
    """Exception raised when there are insufficient funds for an operation."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INSUFFICIENT_FUNDS.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class InsufficientBalanceError(BaseError):
    """Exception raised when an operation fails due to insufficient account balance."""

    def __init__(
        self,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.INSUFFICIENT_BALANCE.value,
        additional_data: dict | None = None,
    ) -> None:
        super().__init__(error, lang, additional_data)


class MaintenanceModeError(BaseError):
    """Exception raised when the system is in maintenance mode."""

    def __init__(
        self,
        estimated_duration: int | None = None,
        lang: LanguageType | None = None,
        error: ErrorDetailDTO = ErrorMessageType.MAINTENANCE_MODE.value,
        additional_data: dict | None = None,
    ) -> None:
        data = {"estimated_duration": estimated_duration} if estimated_duration else {}
        if additional_data:
            data.update(additional_data)
        super().__init__(error, lang, data if data else None)
