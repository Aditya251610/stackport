from pydantic import BaseModel, Field


class TunnelRequest(BaseModel):
    id: str
    method: str
    path: str
    headers: dict[str, str] = Field(default_factory=dict)
    body: str | None = None


class TunnelResponse(BaseModel):
    id: str
    status: int
    headers: dict[str, str] = Field(default_factory=dict)
    body: str | None = None


class TunnelError(BaseModel):
    id: str
    error: str