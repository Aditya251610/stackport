import uuid

from websockets.sync.client import connect

from stackport.models.message import TunnelMessage
from stackport.models.tunnel import (
    TunnelError,
    TunnelRequest,
    TunnelResponse,
)
from stackport.tunnel.forwarder import HTTPForwarder


def main():

    forwarder = HTTPForwarder(
        host="127.0.0.1",
        port=8000,
    )

    request = TunnelRequest(
        id=str(uuid.uuid4()),
        method="GET",
        path="/hello",
        headers={},
        body=None,
    )

    message = TunnelMessage(
        type="request",
        payload=request,
    )

    with connect("ws://localhost:8765") as websocket:

        print(f"Connecting to Stackport server...")
        print(f"Sending: {request}")

        websocket.send(
            message.model_dump_json()
        )

        # Receive request from server.
        raw_message = websocket.recv()

        received_message = TunnelMessage.model_validate_json(
            raw_message
        )

        received_request = received_message.payload

        print(
            f"Received request from server: {received_request}"
        )

        # Forward request to the local application.
        response = forwarder.forward(received_request)

        if isinstance(response, TunnelResponse):

            response_message = TunnelMessage(
                type="response",
                payload=response,
            )

        elif isinstance(response, TunnelError):

            response_message = TunnelMessage(
                type="error",
                payload=response,
            )

        else:

            raise TypeError(
                f"Unexpected response type: {type(response)}"
            )

        print(f"Sending response: {response}")

        websocket.send(
            response_message.model_dump_json()
        )


if __name__ == "__main__":
    main()