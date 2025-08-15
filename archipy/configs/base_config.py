from typing import TypeVar

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from archipy.configs.config_template import (
    AuthConfig,
    DatetimeConfig,
    ElasticsearchAPMConfig,
    ElasticsearchConfig,
    EmailConfig,
    FastAPIConfig,
    FileConfig,
    GrpcConfig,
    KafkaConfig,
    KavenegarConfig,
    KeycloakConfig,
    MinioConfig,
    ParsianShaparakConfig,
    PostgresSQLAlchemyConfig,
    PrometheusConfig,
    RedisConfig,
    SentryConfig,
    SQLAlchemyConfig,
    SQLiteSQLAlchemyConfig,
    StarRocksSQLAlchemyConfig,
)
from archipy.configs.environment_type import EnvironmentType
from archipy.models.types import LanguageType

T = TypeVar("T", bound="BaseConfig")


class BaseConfig(BaseSettings):
    """Base configuration class for ArchiPy applications.

    This class provides a comprehensive configuration system that loads settings
    from multiple sources with a clear priority order. It supports hot-reloading
    and a global singleton pattern for easy access throughout an application.

    Configuration Loading Priority (Highest to Lowest):
    1.  Secret files (e.g., Docker secrets).
    2.  `pyproject.toml` file (`[tool.configs]` section).
    3.  A specified `.toml` file (e.g., `configs.toml`).
    4.  OS-level environment variables.
    5.  `.env` file.
    6.  Default values defined in the class fields.

    The class implements the Singleton pattern via a global config instance that
    can be set once and accessed throughout the application.

    Examples:
        >>> from archipy.configs.base_config import BaseConfig
        >>>
        >>> class MyAppConfig(BaseConfig):
        ...     APP_NAME: str = "My Application"
        ...     DEBUG: bool = True
        >>>
        >>> # Set as global configuration at application startup
        >>> config = MyAppConfig()
        >>> BaseConfig.set_global(config)
        >>>
        >>> # Access from anywhere
        >>> from archipy.configs.base_config import BaseConfig
        >>> current_config = BaseConfig.global_config()
        >>> print(current_config.APP_NAME)
        "My Application"
    """

    model_config = SettingsConfigDict(
        case_sensitive=True,
        pyproject_toml_depth=3,
        env_file=".env",
        pyproject_toml_table_header=("tool", "configs"),
        extra="ignore",
        env_nested_delimiter="__",
        env_ignore_empty=True,
    )

    # --- Singleton State Management ---
    __global_config: T | None = None
    __config_class_to_reload: type[T] | None = None

    # --- Default Configuration Templates ---
    AUTH: AuthConfig = AuthConfig()
    DATETIME: DatetimeConfig = DatetimeConfig()
    ELASTIC: ElasticsearchConfig = ElasticsearchConfig()
    ELASTIC_APM: ElasticsearchAPMConfig = ElasticsearchAPMConfig()
    EMAIL: EmailConfig = EmailConfig()
    ENVIRONMENT: EnvironmentType = EnvironmentType.LOCAL
    FASTAPI: FastAPIConfig = FastAPIConfig()
    FILE: FileConfig = FileConfig()
    GRPC: GrpcConfig = GrpcConfig()
    KAFKA: KafkaConfig = KafkaConfig()
    KAVENEGAR: KavenegarConfig = KavenegarConfig()
    KEYCLOAK: KeycloakConfig = KeycloakConfig()
    MINIO: MinioConfig = MinioConfig()
    PARSIAN_SHAPARAK: ParsianShaparakConfig = ParsianShaparakConfig()
    PROMETHEUS: PrometheusConfig = PrometheusConfig()
    REDIS: RedisConfig = RedisConfig()
    SENTRY: SentryConfig = SentryConfig()
    SQLALCHEMY: SQLAlchemyConfig = SQLAlchemyConfig()
    STARROCKS_SQLALCHEMY: StarRocksSQLAlchemyConfig = StarRocksSQLAlchemyConfig()
    POSTGRES_SQLALCHEMY: PostgresSQLAlchemyConfig = PostgresSQLAlchemyConfig()
    SQLITE_SQLALCHEMY: SQLiteSQLAlchemyConfig = SQLiteSQLAlchemyConfig()
    LANGUAGE: LanguageType = LanguageType.FA

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize the settings sources priority order."""
        return (
            file_secret_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            init_settings,
        )

    def customize(self) -> None:
        """Customize configuration after loading.

        This method can be overridden in subclasses to perform custom
        configuration modifications after loading settings.
        """
        self.ELASTIC_APM.ENVIRONMENT = self.ENVIRONMENT

    @classmethod
    def global_config(cls) -> T:
        """Retrieves the global configuration instance.

        Returns:
            T: The global configuration instance, correctly typed to the subclass.

        Raises:
            AssertionError: If the global config hasn't been set.
        """
        if cls.__global_config is None:
            raise AssertionError("Global config not set. Call BaseConfig.set_global(MyConfig()) first.")
        return cls.__global_config

    @classmethod
    def set_global(cls, config: T) -> None:
        """Sets the global configuration instance and stores its type for reloading.

        This method should be called once during application initialization.

        Args:
            config (T): The configuration instance to use globally.
        """
        if hasattr(config, "customize") and callable(config.customize):
            config.customize()
        cls.__global_config = config
        cls.__config_class_to_reload = type(config)

    @classmethod
    def reload(cls) -> None:
        """Dynamically reloads the global configuration from all sources.

        This method creates a new instance of the registered configuration class,
        allowing the application to pick up changes from environment variables or
        configuration files without needing a restart. It replaces the existing
        global configuration instance with the newly created one.

        This is particularly useful in dynamic environments for tasks such as
        updating feature flags, changing log levels, or responding to
        centralized configuration changes (e.g., from Consul).

        Raises:
            RuntimeError: If the global configuration has not been set yet via
                the `set_global()` method, as the class type to reload would
                be unknown.
        """
        if cls.__config_class_to_reload is None:
            raise RuntimeError("Cannot reload: config was never set with set_global().")

        new_instance = cls.__config_class_to_reload()
        cls.set_global(new_instance)
