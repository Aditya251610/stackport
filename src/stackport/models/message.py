from typing import Literal

from pydantic import BaseModel

from stackport.models.tunnel import (
    TunnelRequest,
    TunnelResponse,
    TunnelError,
)


class TunnelMessage(BaseModel):

    type: Literal["request", "response", "error"]

    payload: TunnelRequest | TunnelResponse | TunnelError