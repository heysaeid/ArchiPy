# Configs

## Overview

The configs module provides tools for standardized configuration management and injection, supporting consistent setup
across services like databases, Redis, and email.

## Quick Start

```python
from archipy.configs.base_config import BaseConfig

class AppConfig(BaseConfig):
    APP_NAME: str = "MyService"
    DEBUG: bool = False
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
```

## API Stability

| Component         | Status    | Notes            |
|-------------------|-----------|------------------|
| BaseConfig        | 🟢 Stable | Production-ready |
| Config Templates  | 🟢 Stable | Production-ready |
| Environment Types | 🟢 Stable | Production-ready |

## Core Classes

### BaseConfig

The main configuration class that provides environment variable support, type validation, and global configuration access.

**Key Features:**
- Environment variable support
- Type validation
- Global configuration access
- Nested configuration support

### SQLAlchemyConfig

Database configuration template with connection settings, pool configuration, and debug options.

**Key Features:**
- Database connection settings
- Pool configuration
- Migration settings
- Debug options

## Examples

For practical examples, see the [Configuration Management Guide](../examples/config_management.md).

## Source Code

📁 Location: `archipy/configs/`

🔗 [Browse Source](https://github.com/SyntaxArc/ArchiPy/tree/master/archipy/configs)
- `ENABLE_FROM_LINTING`: Whether to enable SQL linting
- `HIDE_PARAMETERS`: Whether to hide SQL parameters in logs
- `HOST`: Database host
- `ISOLATION_LEVEL`: Transaction isolation level
- `PASSWORD`: Database password
- `POOL_MAX_OVERFLOW`: Maximum number of connections in pool overflow
- `POOL_PRE_PING`: Whether to ping connections before use
- `POOL_RECYCLE_SECONDS`: Seconds between connection recycling
- `POOL_RESET_ON_RETURN`: Action when returning connections to pool
- `POOL_SIZE`: Number of connections to keep open
- `POOL_TIMEOUT`: Seconds to wait for a connection
- `POOL_USE_LIFO`: Whether to use LIFO for connection pool
- `PORT`: Database port
- `QUERY_CACHE_SIZE`: Size of the query cache
- `USERNAME`: Database username

### SQLiteSQLAlchemyConfig

Class: `archipy.configs.config_template.SQLiteSQLAlchemyConfig`

Configures:

- SQLite-specific database settings
- In-memory database options
- SQLite isolation levels

Attributes:

- `DRIVER_NAME`: SQLite driver name
- `DATABASE`: SQLite database path
- `ISOLATION_LEVEL`: SQLite isolation level
- `PORT`: Not used for SQLite

### PostgresSQLAlchemyConfig

Class: `archipy.configs.config_template.PostgresSQLAlchemyConfig`

Configures:

- PostgreSQL-specific database settings
- Connection URL building
- DSN configuration

Attributes:

- `POSTGRES_DSN`: PostgreSQL connection URL

### StarrocksSQLAlchemyConfig

Class: `archipy.configs.config_template.StarrocksSQLAlchemyConfig`

Configures:

- Starrocks-specific database settings
- Catalog configuration

Attributes:

- `CATALOG`: Starrocks catalog name

### RedisConfig

Class: `archipy.configs.config_template.RedisConfig`

Configures:

- Connection settings
- Pool configuration
- SSL options
- Sentinel support

Attributes:

- `MASTER_HOST`: Redis master host
- `SLAVE_HOST`: Redis slave host
- `PORT`: Redis server port
- `DATABASE`: Redis database number
- `PASSWORD`: Redis password
- `DECODE_RESPONSES`: Whether to decode responses
- `VERSION`: Redis protocol version
- `HEALTH_CHECK_INTERVAL`: Health check interval in seconds

### EmailConfig

Class: `archipy.configs.config_template.EmailConfig`

Configures:

- SMTP settings
- Authentication
- TLS options
- Default headers

Attributes:

- `SMTP_SERVER`: SMTP server host
- `SMTP_PORT`: SMTP server port
- `USERNAME`: SMTP username
- `PASSWORD`: SMTP password
- `POOL_SIZE`: Connection pool size
- `CONNECTION_TIMEOUT`: Connection timeout in seconds
- `MAX_RETRIES`: Maximum retry attempts
- `ATTACHMENT_MAX_SIZE`: Maximum attachment size in bytes

### FastAPIConfig

Class: `archipy.configs.config_template.FastAPIConfig`

Configures:

- API versioning
- CORS configuration
- Rate limiting
- Documentation

Attributes:

- `PROJECT_NAME`: Name of the FastAPI project
- `API_PREFIX`: URL prefix for API endpoints
- `ACCESS_LOG`: Whether to enable access logging
- `BACKLOG`: Maximum number of queued connections
- `DATE_HEADER`: Whether to include date header in responses
- `FORWARDED_ALLOW_IPS`: List of allowed forwarded IPs
- `LIMIT_CONCURRENCY`: Maximum concurrent requests
- `LIMIT_MAX_REQUESTS`: Maximum number of requests
- `CORS_MIDDLEWARE_ALLOW_CREDENTIALS`: Whether to allow credentials in CORS
- `CORS_MIDDLEWARE_ALLOW_HEADERS`: Allowed CORS headers
- `CORS_MIDDLEWARE_ALLOW_METHODS`: Allowed CORS methods
- `CORS_MIDDLEWARE_ALLOW_ORIGINS`: Allowed CORS origins
- `PROXY_HEADERS`: Whether to trust proxy headers
- `RELOAD`: Whether to enable auto-reload
- `SERVER_HEADER`: Whether to include server header
- `SERVE_HOST`: Host to serve the application on
- `SERVE_PORT`: Port to serve the application on
- `TIMEOUT_GRACEFUL_SHUTDOWN`: Graceful shutdown timeout
- `TIMEOUT_KEEP_ALIVE`: Keep-alive timeout
- `WORKERS_COUNT`: Number of worker processes
- `WS_MAX_SIZE`: Maximum WebSocket message size
- `WS_PER_MESSAGE_DEFLATE`: Whether to enable WebSocket compression
- `WS_PING_INTERVAL`: WebSocket ping interval
- `WS_PING_TIMEOUT`: WebSocket ping timeout
- `OPENAPI_URL`: URL for OpenAPI schema
- `DOCS_URL`: URL for API documentation
- `RE_DOCS_URL`: URL for ReDoc documentation
- `SWAGGER_UI_PARAMS`: Swagger UI parameters

### GrpcConfig

Class: `archipy.configs.config_template.GrpcConfig`

Configures:

- Server settings
- Client configuration
- Interceptors
- SSL/TLS options

Attributes:

- `SERVE_PORT`: Port to serve gRPC on
- `SERVE_HOST`: Host to serve gRPC on
- `THREAD_WORKER_COUNT`: Number of worker threads
- `THREAD_PER_CPU_CORE`: Threads per CPU core
- `SERVER_OPTIONS_CONFIG_LIST`: Server configuration options
- `STUB_OPTIONS_CONFIG_LIST`: Client stub configuration options

### SentryConfig

Class: `archipy.configs.config_template.SentryConfig`

Configures:

- DSN configuration
- Environment settings
- Sample rates
- Performance monitoring

Attributes:

- `IS_ENABLED`: Whether Sentry is enabled
- `DSN`: Sentry DSN for error reporting
- `DEBUG`: Whether to enable debug mode
- `RELEASE`: Application release version
- `SAMPLE_RATE`: Error sampling rate (0.0 to 1.0)
- `TRACES_SAMPLE_RATE`: Performance monitoring sampling rate (0.0 to 1.0)

### ElasticsearchConfig

Class: `archipy.configs.config_template.ElasticsearchConfig`

Configures:

- Cluster configuration
- Authentication
- Index settings
- Retry policies

Attributes:

- `SEARCH_HOSTS`: List of Elasticsearch server hosts
- `SEARCH_HTTP_USER_NAME`: Username for HTTP authentication
- `SEARCH_HTTP_PASSWORD`: Password for HTTP authentication
- `SEARCH_HTTPS_VERIFY_CERTS`: Whether to verify SSL certificates
- `SEARCH_KWARG`: Additional keyword arguments for Elasticsearch client
- `SEARCH_BATCH_INTERVAL_THRESHOLD_IN_SECONDS`: Time threshold for batch operations
- `SEARCH_BATCH_DOC_COUNT_THRESHOLD`: Document count threshold for batch operations

### ElasticsearchAPMConfig

Class: `archipy.configs.config_template.ElasticsearchAPMConfig`

Configures:

- APM server settings
- Service name
- Transaction sampling
- Instrumentation

Attributes:

- `API_REQUEST_SIZE`: Maximum size of API requests
- `API_REQUEST_TIME`: Maximum time for API requests
- `AUTO_LOG_STACKS`: Whether to automatically log stack traces
- `CAPTURE_BODY`: Level of request body capture
- `CAPTURE_HEADERS`: Whether to capture HTTP headers
- `COLLECT_LOCAL_VARIABLES`: Level of local variable collection
- `IS_ENABLED`: Whether APM is enabled
- `ENVIRONMENT`: APM environment name
- `LOG_FILE`: Path to APM log file
- `LOG_FILE_SIZE`: Maximum size of APM log file
- `RECORDING`: Whether to record transactions
- `SECRET_TOKEN`: APM secret token
- `SERVER_TIMEOUT`: Server timeout duration
- `SERVER_URL`: APM server URL
- `SERVICE_NAME`: Name of the service being monitored
- `SERVICE_VERSION`: Version of the service
- `TRANSACTION_SAMPLE_RATE`: Rate at which to sample transactions
- `API_KEY`: API key for authentication

### KafkaConfig

Class: `archipy.configs.config_template.KafkaConfig`

Configures:

- Broker configuration
- Consumer groups
- Producer settings
- Security options

Attributes:

- `ACKNOWLEDGE_COUNT`: Number of acknowledgments required
- `AUTO_OFFSET_RESET`: Action to take when there is no initial offset
- `BROKERS_LIST`: List of Kafka broker addresses
- `CERT_PEM`: Path to SSL certificate
- `ENABLE_AUTO_COMMIT`: Whether to enable auto-commit
- `MAX_BUFFER_MS`: Maximum time to buffer messages
- `MAX_BUFFER_SIZE`: Maximum number of messages to buffer
- `PASSWORD`: Password for authentication
- `SASL_MECHANISMS`: SASL mechanism for authentication
- `SECURITY_PROTOCOL`: Security protocol to use
- `SESSION_TIMEOUT_MS`: Session timeout in milliseconds
- `REQUEST_ACK_TIMEOUT_MS`: Request acknowledgment timeout
- `DELIVERY_MESSAGE_TIMEOUT_MS`: Message delivery timeout
- `USER_NAME`: Username for authentication
- `LIST_TOPICS_TIMEOUT`: Timeout for listing topics

### KeycloakConfig

Class: `archipy.configs.config_template.KeycloakConfig`

Configures:

- Server connection
- Authentication settings
- SSL verification
- Timeout configuration

Attributes:

- `SERVER_URL`: URL of the Keycloak server
- `CLIENT_ID`: Client ID for authentication
- `REALM_NAME`: Name of the Keycloak realm
- `CLIENT_SECRET_KEY`: Client secret key
- `VERIFY_SSL`: Whether to verify SSL certificates
- `TIMEOUT`: Request timeout in seconds

### MinioConfig

Class: `archipy.configs.config_template.MinioConfig`

Configures:

- Server connection
- Authentication
- Security settings
- Region configuration

Attributes:

- `ENDPOINT`: MinIO server endpoint
- `ACCESS_KEY`: Access key for authentication
- `SECRET_KEY`: Secret key for authentication
- `SECURE`: Whether to use secure (HTTPS) connection
- `SESSION_TOKEN`: Session token for temporary credentials
- `REGION`: AWS region for S3 compatibility

### PrometheusConfig

Class: `archipy.configs.config_template.PrometheusConfig`

Configures:

- Metrics collection
- Server settings
- Endpoint configuration

Attributes:

- `IS_ENABLED`: Whether Prometheus metrics are enabled
- `SERVER_PORT`: Port for the Prometheus metrics endpoint

### KavenegarConfig

Class: `archipy.configs.config_template.KavenegarConfig`

Configures:

- API connection
- Authentication
- Default sender settings

Attributes:

- `SERVER_URL`: Kavenegar API server URL
- `API_KEY`: Kavenegar API key
- `PHONE_NUMBER`: Default sender phone number

### AuthConfig

Class: `archipy.configs.config_template.AuthConfig`

Configures:

- JWT settings
- TOTP configuration
- Rate limiting
- Password policies
- Token security

Attributes:

- `SECRET_KEY`: JWT signing key
- `ACCESS_TOKEN_EXPIRES_IN`: Access token expiration in seconds
- `REFRESH_TOKEN_EXPIRES_IN`: Refresh token expiration in seconds
- `HASH_ALGORITHM`: JWT signing algorithm
- `JWT_ISSUER`: JWT issuer claim
- `JWT_AUDIENCE`: JWT audience claim
- `TOKEN_VERSION`: JWT token version
- `TOTP_SECRET_KEY`: TOTP master key
- `TOTP_HASH_ALGORITHM`: TOTP hash algorithm
- `TOTP_LENGTH`: TOTP code length
- `TOTP_EXPIRES_IN`: TOTP expiration in seconds
- `TOTP_TIME_STEP`: TOTP time step in seconds
- `TOTP_VERIFICATION_WINDOW`: TOTP verification window size
- `TOTP_MAX_ATTEMPTS`: Maximum TOTP verification attempts
- `TOTP_LOCKOUT_TIME`: TOTP lockout duration in seconds
- `LOGIN_RATE_LIMIT`: Login attempts per minute
- `TOTP_RATE_LIMIT`: TOTP requests per minute
- `PASSWORD_RESET_RATE_LIMIT`: Password reset requests per hour
- `HASH_ITERATIONS`: Password hash iterations
- `MIN_LENGTH`: Minimum password length
- `REQUIRE_DIGIT`: Whether password requires digits
- `REQUIRE_LOWERCASE`: Whether password requires lowercase
- `REQUIRE_SPECIAL`: Whether password requires special chars
- `REQUIRE_UPPERCASE`: Whether password requires uppercase
- `SALT_LENGTH`: Password salt length
- `SPECIAL_CHARACTERS`: Allowed special characters
- `PASSWORD_HISTORY_SIZE`: Number of previous passwords to remember
- `ENABLE_JTI_CLAIM`: Whether to enable JWT ID claim
- `ENABLE_TOKEN_ROTATION`: Whether to enable refresh token rotation
- `REFRESH_TOKEN_REUSE_INTERVAL`: Refresh token reuse grace period

### FileConfig

Class: `archipy.configs.config_template.FileConfig`

Configures:

- File link security
- Expiration policies
- File type restrictions

Attributes:

- `SECRET_KEY`: Secret key for generating secure file links
- `DEFAULT_EXPIRY_MINUTES`: Default link expiration time in minutes
- `ALLOWED_EXTENSIONS`: List of allowed file extensions

### DatetimeConfig

Class: `archipy.configs.config_template.DatetimeConfig`

Configures:

- API connections
- Time service settings
- Caching behavior

Attributes:

- `TIME_IR_API_KEY`: API key for time.ir service
- `TIME_IR_API_ENDPOINT`: Endpoint for time.ir service
- `REQUEST_TIMEOUT`: Request timeout in seconds
- `MAX_RETRIES`: Maximum retry attempts
- `CACHE_TTL`: Cache time-to-live in seconds
- `HISTORICAL_CACHE_TTL`: Cache time-to-live for historical dates in seconds

### EnvironmentType

Class: `archipy.configs.environment_type.EnvironmentType`

Configures:

- Environment types (DEV, STAGING, PROD)
- Environment-specific behaviors
- Configuration validation rules

*Includes all members, undocumented members, and shows inheritance.*
