import functools
import logging
from collections.abc import Callable
from contextvars import ContextVar
from typing import Any

try:
    import grpc
    from grpc import ServicerContext
    from grpc.aio import ServicerContext as AsyncServicerContext

except ImportError:
    ServicerContext = None
    AsyncServicerContext = None

from fastapi import Depends, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from archipy.adapters.keycloak.adapters import AsyncKeycloakAdapter, KeycloakAdapter
from archipy.models.errors import (
    BaseError,
    InternalError,
    InvalidArgumentError,
    PermissionDeniedError,
    TokenExpiredError,
    UnauthenticatedError,
)
from archipy.models.types.language_type import LanguageType

# Enhanced security scheme with OpenAPI documentation
security = HTTPBearer(scheme_name="OAuth2", description="OAuth2 Access Token", auto_error=False)

# Default language for errors
DEFAULT_LANG = LanguageType.FA

logger = logging.getLogger(__name__)


class AuthContext(BaseModel):
    """Authentication context passed to business logic."""

    user_id: str
    username: str
    email: str
    roles: list[str]
    token: str
    raw_user_info: dict[str, Any]


# Solution 1: Using contextvars (Recommended)
_auth_context_var: ContextVar[AuthContext | None] = ContextVar("auth_context", default=None)


class AuthContextManager:
    """Manager for handling auth context in gRPC services."""

    @staticmethod
    def set_auth_context(auth_context: AuthContext) -> None:
        """Set the auth context for the current request."""
        _auth_context_var.set(auth_context)

    @staticmethod
    def get_auth_context() -> AuthContext | None:
        """Get the auth context for the current request."""
        return _auth_context_var.get()

    @staticmethod
    def clear_auth_context() -> None:
        """Clear the auth context for the current request."""
        _auth_context_var.set(None)


class KeycloakUtils:
    """Utility class for Keycloak authentication and authorization in FastAPI applications."""

    @staticmethod
    def _get_keycloak_adapter() -> KeycloakAdapter:
        return KeycloakAdapter()

    @staticmethod
    def _get_async_keycloak_adapter() -> AsyncKeycloakAdapter:
        return AsyncKeycloakAdapter()

    @classmethod
    # Synchronous decorator
    def fastapi_auth(
        cls,
        resource_type_param: str | None = None,
        resource_type: str | None = None,
        required_roles: frozenset[str] | None = None,
        all_roles_required: bool = False,
        required_permissions: tuple[tuple[str, str], ...] | None = None,
        admin_roles: frozenset[str] | None = None,
        lang: LanguageType = DEFAULT_LANG,
    ) -> Callable:
        """FastAPI decorator for Keycloak authentication and resource-based authorization.

        Args:
            resource_type_param: The parameter name in the path (e.g., 'user_uuid', 'employee_uuid')
            resource_type: The type of resource being accessed (e.g., 'users', 'employees')
            required_roles: Set of role names that the user must have
            all_roles_required: If True, user must have all specified roles; if False, any role is sufficient
            required_permissions: List of (resource, scope) tuples to check
            admin_roles: Set of roles that grant administrative access to all resources
            lang: Language for error messages
        Raises:
            UnauthenticatedError: If no valid Authorization header is provided
            InvalidTokenError: If token is invalid
            TokenExpiredError: If token is expired
            PermissionDeniedError: If user lacks required roles, permissions, or resource access
            InvalidArgumentError: If resource_type_param is missing when resource_type is provided
        """

        def dependency(
            request: Request,
            token: HTTPAuthorizationCredentials = Security(security),
            keycloak: KeycloakAdapter = Depends(cls._get_keycloak_adapter),
        ) -> dict:
            if token is None:
                raise UnauthenticatedError(lang=lang)
            token_str = token.credentials  # Extract the token string
            # Validate token
            if not keycloak.validate_token(token_str):
                token_info = keycloak.introspect_token(token_str)
                if not token_info.get("active", False):
                    raise TokenExpiredError(lang=lang)

            # Get user info from token
            user_info = keycloak.get_userinfo(token_str)
            token_info = keycloak.get_token_info(token_str)

            # Resource-based authorization if resource type is provided
            if resource_type and resource_type_param:
                # Extract resource UUID from path parameters
                resource_uuid = request.path_params.get(resource_type_param)
                if not resource_uuid:
                    raise InvalidArgumentError(argument_name=resource_type_param, lang=lang)

                # Verify resource exists and user has access
                user_uuid = user_info.get("sub")

                # Check if resource exists
                resource_user = keycloak.get_user_by_id(resource_uuid)
                if not resource_user:
                    raise PermissionDeniedError(
                        lang=lang,
                        additional_data={"resource_type": resource_type, "resource_id": resource_uuid},
                    )

                # Authorization check: either owns the resource or has admin privileges
                has_admin_privileges = admin_roles and keycloak.has_any_of_roles(token_str, admin_roles)
                if user_uuid != resource_uuid and not has_admin_privileges:
                    raise PermissionDeniedError(
                        lang=lang,
                        additional_data={"resource_type": resource_type, "resource_id": resource_uuid},
                    )

            # Check additional roles if specified
            if required_roles:
                if all_roles_required:
                    if not keycloak.has_all_roles(token_str, required_roles):
                        raise PermissionDeniedError(
                            lang=lang,
                            additional_data={"required_roles": required_roles},
                        )
                elif not keycloak.has_any_of_roles(token_str, required_roles):
                    raise PermissionDeniedError(
                        lang=lang,
                        additional_data={"required_roles": required_roles},
                    )

            # Check permissions if specified
            if required_permissions:
                for resource, scope in required_permissions:
                    if not keycloak.check_permissions(token_str, resource, scope):
                        raise PermissionDeniedError(
                            lang=lang,
                            additional_data={"required_permission": f"{resource}#{scope}"},
                        )

            # Add user info to request state
            request.state.user_info = user_info
            request.state.token_info = token_info
            request.state.user_uuid = user_info.get("sub", None)
            return user_info

        return dependency

    @classmethod
    def async_fastapi_auth(
        cls,
        resource_type_param: str | None = None,
        resource_type: str | None = None,
        required_roles: frozenset[str] | None = None,
        all_roles_required: bool = False,
        required_permissions: tuple[tuple[str, str], ...] | None = None,
        admin_roles: frozenset[str] | None = None,
        lang: LanguageType = DEFAULT_LANG,
    ) -> Callable:
        """FastAPI async decorator for Keycloak authentication and resource-based authorization.

        Args:
            resource_type_param: The parameter name in the path (e.g., 'user_uuid', 'employee_uuid')
            resource_type: The type of resource being accessed (e.g., 'users', 'employees')
            required_roles: Set of role names that the user must have
            all_roles_required: If True, user must have all specified roles; if False, any role is sufficient
            required_permissions: List of (resource, scope) tuples to check
            admin_roles: Set of roles that grant administrative access to all resources
            lang: Language for error messages
        Raises:
            UnauthenticatedError: If no valid Authorization header is provided
            InvalidTokenError: If token is invalid
            TokenExpiredError: If token is expired
            PermissionDeniedError: If user lacks required roles, permissions, or resource access
            InvalidArgumentError: If resource_type_param is missing when resource_type is provided
        """

        async def dependency(
            request: Request,
            token: HTTPAuthorizationCredentials = Security(security),
            keycloak: AsyncKeycloakAdapter = Depends(cls._get_async_keycloak_adapter),
        ) -> dict:
            if token is None:
                raise UnauthenticatedError(lang=lang)
            token_str = token.credentials  # Extract the token string

            # Validate token
            if not await keycloak.validate_token(token_str):
                # Handle token validation error
                token_info = await keycloak.introspect_token(token_str)
                if not token_info.get("active", False):
                    raise TokenExpiredError(lang=lang)

            # Get user info from token
            user_info = await keycloak.get_userinfo(token_str)
            token_info = await keycloak.get_token_info(token_str)

            # Resource-based authorization if resource type is provided
            if resource_type and resource_type_param:
                # Extract resource UUID from path parameters
                resource_uuid = request.path_params.get(resource_type_param)
                if not resource_uuid:
                    raise InvalidArgumentError(argument_name=resource_type_param, lang=lang)

                # Verify resource exists and user has access
                user_uuid = user_info.get("sub")

                # Check if resource exists
                resource_user = await keycloak.get_user_by_id(resource_uuid)
                if not resource_user:
                    raise PermissionDeniedError(
                        lang=lang,
                        additional_data={"resource_type": resource_type, "resource_id": resource_uuid},
                    )

                # Authorization check: either owns the resource or has admin privileges
                has_admin_privileges = admin_roles and await keycloak.has_any_of_roles(token_str, admin_roles)
                if user_uuid != resource_uuid and not has_admin_privileges:
                    raise PermissionDeniedError(
                        lang=lang,
                        additional_data={"resource_type": resource_type, "resource_id": resource_uuid},
                    )

            # Check additional roles if specified
            if required_roles:
                if all_roles_required:
                    if not await keycloak.has_all_roles(token_str, required_roles):
                        raise PermissionDeniedError(
                            lang=lang,
                            additional_data={"required_roles": required_roles},
                        )
                elif not await keycloak.has_any_of_roles(token_str, required_roles):
                    raise PermissionDeniedError(
                        lang=lang,
                        additional_data={"required_roles": required_roles},
                    )

            # Check permissions if specified
            if required_permissions:
                for resource, scope in required_permissions:
                    if not await keycloak.check_permissions(token_str, resource, scope):
                        raise PermissionDeniedError(
                            lang=lang,
                            additional_data={"required_permission": f"{resource}#{scope}"},
                        )

            # Add user info to request state
            request.state.user_info = user_info
            request.state.token_info = token_info
            request.state.user_uuid = user_info.get("sub", None)
            return user_info

        return dependency

    @staticmethod
    def _extract_token_from_metadata(context: ServicerContext) -> str | None:
        """Extract Bearer token from gRPC metadata."""
        metadata = dict(context.invocation_metadata())

        auth_keys = ["authorization", "Authorization", "auth", "token"]

        for key in auth_keys:
            if key in metadata:
                auth_value = metadata[key]
                if auth_value.startswith("Bearer "):
                    return auth_value[7:]
                elif auth_value.startswith("bearer "):
                    return auth_value[7:]
                else:
                    return auth_value

        return None

    @classmethod
    def grpc_auth(
        cls,
        required_roles: frozenset[str] | None = None,
        all_roles_required: bool = False,
        required_permissions: tuple[tuple[str, str], ...] | None = None,
        resource_attribute_name: str | None = None,
        admin_roles: frozenset[str] | None = None,
        lang: LanguageType = DEFAULT_LANG,
    ) -> Callable[[Callable], Callable]:
        """Synchronous gRPC decorator for authentication and authorization.

        This decorator handles:
        1. Token validation
        2. Role/permission checking
        3. Passing auth context to business logic

        Resource ownership is handled in the business logic layer.

        Args:
            required_roles: Set of roles, user must have at least one (or all if all_roles_required=True)
            all_roles_required: If True, user must have all required_roles; if False, any one role is sufficient
            required_permissions: Tuple of (resource, scope) pairs that must be satisfied
            resource_attribute_name: Attribute name to extract resource UUID from context for ownership checking
            admin_roles: Set of admin roles that bypass resource ownership checks
            lang: Language for error messages

        Returns:
            Decorated function with authentication and authorization
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(self: object, request: object, context: ServicerContext) -> object:
                try:
                    # 1. Extract and validate token
                    token_str = cls._extract_token_from_metadata(context)
                    if not token_str:
                        raise UnauthenticatedError(lang=lang)

                    # 2. Get Keycloak adapter (synchronous)
                    keycloak: KeycloakAdapter = cls._get_keycloak_adapter()

                    # 3. Validate token
                    if not keycloak.validate_token(token_str):
                        token_info = keycloak.introspect_token(token_str)
                        if not token_info.get("active", False):
                            raise TokenExpiredError(lang=lang)

                    # 4. Get user info from token
                    user_info = keycloak.get_userinfo(token_str)

                    # 5. Resource-based authorization if resource_attribute_name is provided
                    if resource_attribute_name:
                        # Extract resource UUID from context
                        resource_uuid = getattr(request, resource_attribute_name)
                        if not resource_uuid:
                            raise InvalidArgumentError(argument_name=resource_attribute_name, lang=lang)

                        # Verify resource exists and user has access
                        user_uuid = user_info.get("sub")

                        # Check if resource exists
                        resource_user = keycloak.get_user_by_id(resource_uuid)
                        if not resource_user:
                            raise PermissionDeniedError(
                                lang=lang,
                                additional_data={"resource_id": resource_uuid},
                            )

                        # Authorization check: either owns the resource or has admin privileges
                        has_admin_privileges = admin_roles and keycloak.has_any_of_roles(token_str, admin_roles)
                        if user_uuid != resource_uuid and not has_admin_privileges:
                            raise PermissionDeniedError(lang=lang, additional_data={"resource_id": resource_uuid})

                    # 6. Check roles if specified
                    if required_roles:
                        if all_roles_required:
                            if not keycloak.has_all_roles(token_str, required_roles):
                                raise PermissionDeniedError(
                                    lang=lang,
                                    additional_data={
                                        "required_roles": list(required_roles),
                                        "check_type": "all_required",
                                    },
                                )

                        elif not keycloak.has_any_of_roles(token_str, required_roles):
                            raise PermissionDeniedError(
                                lang=lang,
                                additional_data={"required_roles": list(required_roles), "check_type": "any_required"},
                            )

                    # 7. Check permissions if specified
                    if required_permissions:
                        for resource, scope in required_permissions:
                            if not keycloak.check_permissions(token_str, resource, scope):
                                raise PermissionDeniedError(
                                    lang=lang,
                                    additional_data={
                                        "required_permission": f"{resource}#{scope}",
                                        "resource": resource,
                                        "scope": scope,
                                    },
                                )

                    # 8. Create auth context for business logic
                    auth_context = AuthContext(
                        user_id=user_info.get("sub"),
                        username=user_info.get("preferred_username", ""),
                        email=user_info.get("email", ""),
                        roles=user_info.get("realm_access", {}).get("roles", []),
                        token=token_str,
                        raw_user_info=user_info,
                    )

                    # 9. Set auth context using contextvars
                    AuthContextManager.set_auth_context(auth_context)

                    # 10. Call the original method - business logic handles ownership
                    return func(self, request, context)

                except Exception as e:
                    if isinstance(e, BaseError):
                        e.abort_grpc_sync(context)
                    raise InternalError(
                        lang=lang,
                        additional_data={"original_error": str(e), "error_type": type(e).__name__},
                    ) from e

                finally:
                    # Clean up auth context
                    AuthContextManager.clear_auth_context()

            return wrapper

        return decorator

    @classmethod
    def async_grpc_auth(
        cls,
        required_roles: frozenset[str] | None = None,
        all_roles_required: bool = False,
        required_permissions: tuple[tuple[str, str], ...] | None = None,
        resource_attribute_name: str | None = None,
        admin_roles: frozenset[str] | None = None,
        lang: LanguageType = DEFAULT_LANG,
    ) -> Callable[[Callable], Callable]:
        """Simplified gRPC decorator for authentication and authorization.

        This decorator handles:
        1. Token validation
        2. Role/permission checking
        3. Passing auth context to business logic

        Resource ownership is handled in the business logic layer.

        Args:
            required_roles: Set of roles, user must have at least one (or all if all_roles_required=True)
            all_roles_required: If True, user must have all required_roles; if False, any one role is sufficient
            required_permissions: Tuple of (resource, scope) pairs that must be satisfied
            resource_attribute_name: Attribute name to extract resource UUID from context for ownership checking
            admin_roles: Set of admin roles that bypass resource ownership checks
            lang: Language for error messages

        Returns:
            Decorated function with authentication and authorization
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(self: object, request: object, context: AsyncServicerContext) -> object:
                try:
                    # 1. Extract and validate token
                    token_str = cls._extract_token_from_metadata(context)
                    if not token_str:
                        raise UnauthenticatedError(lang=lang)

                    # 2. Get Keycloak adapter
                    keycloak: AsyncKeycloakAdapter = cls._get_async_keycloak_adapter()

                    # 3. Validate token
                    if not await keycloak.validate_token(token_str):
                        token_info = await keycloak.introspect_token(token_str)
                        if not token_info.get("active", False):
                            raise TokenExpiredError(lang=lang)

                    # 4. Get user info from token
                    user_info = await keycloak.get_userinfo(token_str)

                    # 5. Resource-based authorization if resource_attribute_name is provided
                    if resource_attribute_name:
                        # Extract resource UUID from context
                        resource_uuid = getattr(request, resource_attribute_name)
                        if not resource_uuid:
                            raise InvalidArgumentError(argument_name=resource_attribute_name, lang=lang)

                        # Verify resource exists and user has access
                        user_uuid = user_info.get("sub")

                        # Check if resource exists
                        resource_user = await keycloak.get_user_by_id(resource_uuid)
                        if not resource_user:
                            raise PermissionDeniedError(
                                lang=lang,
                                additional_data={"resource_id": resource_uuid},
                            )

                        # Authorization check: either owns the resource or has admin privileges
                        has_admin_privileges = admin_roles and await keycloak.has_any_of_roles(token_str, admin_roles)
                        if user_uuid != resource_uuid and not has_admin_privileges:
                            raise PermissionDeniedError(lang=lang, additional_data={"resource_id": resource_uuid})

                    # 6. Check roles if specified
                    if required_roles:
                        if all_roles_required:
                            if not await keycloak.has_all_roles(token_str, required_roles):
                                raise PermissionDeniedError(
                                    lang=lang,
                                    additional_data={
                                        "required_roles": list(required_roles),
                                        "check_type": "all_required",
                                    },
                                )

                        elif not await keycloak.has_any_of_roles(token_str, required_roles):
                            raise PermissionDeniedError(
                                lang=lang,
                                additional_data={"required_roles": list(required_roles), "check_type": "any_required"},
                            )

                    # 7. Check permissions if specified
                    if required_permissions:
                        for resource, scope in required_permissions:
                            if not await keycloak.check_permissions(token_str, resource, scope):
                                raise PermissionDeniedError(
                                    lang=lang,
                                    additional_data={
                                        "required_permission": f"{resource}#{scope}",
                                        "resource": resource,
                                        "scope": scope,
                                    },
                                )

                    # 8. Create auth context for business logic
                    auth_context = AuthContext(
                        user_id=user_info.get("sub"),
                        username=user_info.get("preferred_username", ""),
                        email=user_info.get("email", ""),
                        roles=user_info.get("realm_access", {}).get("roles", []),
                        token=token_str,
                        raw_user_info=user_info,
                    )

                    # 9. Set auth context using contextvars
                    AuthContextManager.set_auth_context(auth_context)

                    # 10. Call the original method - business logic handles ownership
                    return await func(self, request, context)

                except Exception as e:
                    if isinstance(e, BaseError):
                        await e.abort_grpc_async(context)
                    await InternalError(
                        lang=lang,
                        additional_data={"original_error": str(e), "error_type": type(e).__name__},
                    ).abort_grpc_async(context)

                finally:
                    # Clean up auth context
                    AuthContextManager.clear_auth_context()

            return wrapper

        return decorator
