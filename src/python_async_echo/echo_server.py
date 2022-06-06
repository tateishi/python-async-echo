import asyncio

from fire import Fire


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info("peername")

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def echo_main():
    server = await asyncio.start_server(handle_echo, "127.0.0.1", 8888)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Servind on {addrs}")

    async with server:
        await server.serve_forever()


def main():
    def run_echo():
        asyncio.run(echo_main())

    Fire(run_echo)
