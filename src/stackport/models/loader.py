from pydantic import BaseModel, ConfigDict, Field

# app yaml validator
class App(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command: str = Field(
        description="Command to run the application",
        min_length=1,
    )
    port: int = Field(
        description="Port number for the application",
        gt=0,
        le=65535,
    )

# localstack yaml validator
class LocalStack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    services: list[str] = Field(
        description="LocalStack services",
        min_length=1,
    )

# scripts yaml validator
class Scripts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # This needs a different approach because script names are dynamic.

# root validator
class LoaderConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: int = Field(default=1)
    name: str = Field(
        description="Name of the application",
        min_length=1,
    )
    app: App
    localstack: LocalStack | None = None
    scripts: dict[str, str] | None = None