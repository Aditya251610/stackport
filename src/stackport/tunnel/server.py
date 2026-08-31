import asyncio
import os

from websockets.asyncio.server import serve

from stackport.models.message import TunnelMessage


async def tunnel_handler(websocket):

    print("Tunnel client connected.", flush=True)

    try:

        async for raw_message in websocket:

            message = TunnelMessage.model_validate_json(
                raw_message
            )

            print(
                f"Received: {message.type}",
                flush=True,
            )

            # Relay the message back to the connected client.
            await websocket.send(
                message.model_dump_json()
            )

    except Exception as exc:

        print(
            f"Tunnel connection error: {exc}",
            flush=True,
        )

    finally:

        print(
            "Tunnel client disconnected.",
            flush=True,
        )


async def main():

    host = os.environ.get("STACKPORT_HOST", "0.0.0.0")
    port = int(os.environ.get("STACKPORT_PORT", "8765"))

    server = await serve(
        tunnel_handler,
        host,
        port,
    )

    print(
        f"Stackport tunnel server listening on ws://{host}:{port}",
        flush=True,
    )

    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())