from collections.abc import Callable

import elasticapm
import grpc

from archipy.configs.base_config import BaseConfig
from archipy.helpers.interceptors.grpc.base.server_interceptor import (
    BaseAsyncGrpcServerInterceptor,
    BaseGrpcServerInterceptor,
    MethodName,
)
from archipy.helpers.utils.base_utils import BaseUtils


class GrpcServerTraceInterceptor(BaseGrpcServerInterceptor):
    """A gRPC server interceptor for tracing requests using Elastic APM.

    This interceptor captures and traces gRPC server requests, enabling distributed tracing
    across services. It integrates with Elastic APM to monitor and log transactions.
    """

    def intercept(
        self, method: Callable, request: object, context: grpc.ServicerContext, method_name_model: MethodName
    ) -> object:
        """Intercepts a gRPC server call to trace the request using Elastic APM.

        Args:
            method (Callable): The gRPC method being intercepted.
            request (object): The request object passed to the method.
            context (grpc.ServicerContext): The context of the gRPC call.
            method_name_model (MethodName): The parsed method name containing package, service, and method components.

        Returns:
            object: The result of the intercepted gRPC method.

        Raises:
            Exception: If an exception occurs during the method execution, it is captured and logged.

        Notes:
            - If Elastic APM is disabled, the interceptor does nothing and passes the call through.
            - If a trace parent header is present in the metadata, it is used to link the transaction
              to the distributed trace.
            - If no trace parent header is present, a new transaction is started.
        """
        try:
            # Skip tracing if Elastic APM is disabled
            config = BaseConfig.global_config()
            if not config.ELASTIC_APM.IS_ENABLED:
                return method(request, context)

            # Get the Elastic APM client
            client = elasticapm.Client(config.ELASTIC_APM.model_dump())

            # Convert metadata to a dictionary for easier access
            metadata_dict = dict(context.invocation_metadata())

            # Check if a trace parent header is present in the metadata
            if parent := elasticapm.trace_parent_from_headers(metadata_dict):
                # Start a transaction linked to the distributed trace
                client.begin_transaction(transaction_type="request", trace_parent=parent)
                try:
                    # Execute the gRPC method
                    result = method(request, context)

                    # End the transaction with a success status
                    client.end_transaction(name=method_name_model.full_name, result="success")
                except Exception:
                    # End the transaction with a failure status if an exception occurs
                    client.end_transaction(name=method_name_model.full_name, result="failure")
                    raise
                else:
                    return result
            else:
                # Start a new transaction if no trace parent header is present
                client.begin_transaction(transaction_type="request")
                try:
                    # Execute the gRPC method
                    result = method(request, context)

                    # End the transaction with a success status
                    client.end_transaction(name=method_name_model.full_name, result="success")
                except Exception:
                    # End the transaction with a failure status if an exception occurs
                    client.end_transaction(name=method_name_model.full_name, result="failure")
                    raise
                else:
                    return result

        except Exception as exception:
            BaseUtils.capture_exception(exception)
            raise


class AsyncGrpcServerTraceInterceptor(BaseAsyncGrpcServerInterceptor):
    """An async gRPC server interceptor for tracing requests using Elastic APM.

    This interceptor captures and traces async gRPC server requests, enabling distributed tracing
    across services. It integrates with Elastic APM to monitor and log transactions.
    """

    async def intercept(
        self, method: Callable, request: object, context: grpc.aio.ServicerContext, method_name_model: MethodName
    ) -> object:
        """Intercepts an async gRPC server call to trace the request using Elastic APM.

        Args:
            method (Callable): The async gRPC method being intercepted.
            request (object): The request object passed to the method.
            context (grpc.aio.ServicerContext): The context of the async gRPC call.
            method_name_model (MethodName): The parsed method name containing package, service, and method components.

        Returns:
            object: The result of the intercepted gRPC method.

        Raises:
            Exception: If an exception occurs during the method execution, it is captured and logged.

        Notes:
            - If Elastic APM is disabled, the interceptor does nothing and passes the call through.
            - If a trace parent header is present in the metadata, it is used to link the transaction
              to the distributed trace.
            - If no trace parent header is present, a new transaction is started.
        """
        try:
            # Skip tracing if Elastic APM is disabled
            config = BaseConfig.global_config()
            if not config.ELASTIC_APM.IS_ENABLED:
                return await method(request, context)

            # Get the Elastic APM client
            client = elasticapm.Client(config.ELASTIC_APM.model_dump())

            # Convert metadata to a dictionary for easier access
            metadata_dict = dict(context.invocation_metadata())

            # Check if a trace parent header is present in the metadata
            if parent := elasticapm.trace_parent_from_headers(metadata_dict):
                # Start a transaction linked to the distributed trace
                client.begin_transaction(transaction_type="request", trace_parent=parent)
                try:
                    # Execute the async gRPC method
                    result = await method(request, context)

                    # End the transaction with a success status
                    client.end_transaction(name=method_name_model.full_name, result="success")
                except Exception:
                    # End the transaction with a failure status if an exception occurs
                    client.end_transaction(name=method_name_model.full_name, result="failure")
                    raise
                else:
                    return result
            else:
                # Start a new transaction if no trace parent header is present
                client.begin_transaction(transaction_type="request")
                try:
                    # Execute the async gRPC method
                    result = await method(request, context)

                    # End the transaction with a success status
                    client.end_transaction(name=method_name_model.full_name, result="success")
                except Exception:
                    # End the transaction with a failure status if an exception occurs
                    client.end_transaction(name=method_name_model.full_name, result="failure")
                    raise
                else:
                    return result

        except Exception as exception:
            BaseUtils.capture_exception(exception)
            raise  # Re-raise the exception to maintain proper error handling
