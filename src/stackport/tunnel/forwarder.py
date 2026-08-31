import requests

from stackport.models.tunnel import (
    TunnelError,
    TunnelRequest,
    TunnelResponse,
)


class HTTPForwarder:

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.base_url = f"http://{host}:{port}"

    def forward(
        self,
        request: TunnelRequest,
    ) -> TunnelResponse | TunnelError:

        try:
            response = requests.request(
                method=request.method.upper(),
                url=f"{self.base_url}{request.path}",
                headers=request.headers,
                data=request.body,
                timeout=30,
            )

            return TunnelResponse(
                id=request.id,
                status=response.status_code,
                headers=dict(response.headers),
                body=response.text,
            )

        except requests.RequestException as exc:
            return TunnelError(
                id=request.id,
                error=str(exc),
            )