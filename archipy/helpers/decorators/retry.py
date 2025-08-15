import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar, cast

from archipy.models.errors import ResourceExhaustedError

# Define a type variable for the return type of the decorated function
F = TypeVar("F", bound=Callable[..., Any])


def retry_decorator(
    max_retries: int = 3,
    delay: float = 1,
    retry_on: tuple[type[Exception], ...] | None = None,
    ignore: tuple[type[Exception], ...] | None = None,
    resource_type: str | None = None,
) -> Callable[[F], F]:
    """A decorator that retries a function when it raises an exception.

    Args:
        max_retries (int): The maximum number of retry attempts. Defaults to 3.
        delay (float): The delay (in seconds) between retries. Defaults to 1.
        retry_on (Optional[Tuple[Type[Exception], ...]]): A tuple of errors to retry on.
            If None, retries on all errors. Defaults to None.
        ignore (Optional[Tuple[Type[Exception], ...]]): A tuple of errors to ignore (not retry on).
            If None, no errors are ignored. Defaults to None.
        resource_type (Optional[str]): The type of resource being exhausted. Defaults to None.
        lang (str): The language for the error message (default: "fa").

    Returns:
        Callable: The decorated function with retry logic.

    Example:
        To use this decorator, apply it to a function:

        ```python
        @retry_decorator(max_retries=3, delay=1, retry_on=(ValueError,), ignore=(TypeError,), resource_type="API")
        def unreliable_function():
            if random.random() < 0.5:
                raise ValueError("Temporary failure")
            return "Success"

        result = unreliable_function()
        ```

        Output:
        ```
        2023-10-10 12:00:00,000 - WARNING - Attempt 1 failed: Temporary failure
        2023-10-10 12:00:01,000 - INFO - Attempt 2 succeeded.
        Success
        ```
    """

    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    if retries > 0:
                        logging.info("Attempt %d succeeded.", retries + 1)
                except Exception as e:
                    retries += 1
                    # Check if the exception should be ignored
                    if ignore and isinstance(e, ignore):
                        raise
                    # Check if the exception should be retried
                    if retry_on and not isinstance(e, retry_on):
                        raise
                    logging.warning("Attempt %d failed: %s", retries, e)
                    if retries < max_retries:
                        time.sleep(delay)
                    continue
                return result
            raise ResourceExhaustedError(resource_type=resource_type)

        return cast(F, wrapper)

    return decorator
