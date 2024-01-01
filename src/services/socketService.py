import threading

import websockets
import asyncio


class SocketClient:
    def __init__(self, uri, message_callback):
        self.uri = uri
        self.websocket = None
        self.task_queue = asyncio.Queue()
        self.message_callback = message_callback

        # Create and start a thread for the WebSocket client
        self.websocket_thread = threading.Thread(target=self.start_websocket_client)
        self.websocket_thread.start()

    def start_websocket_client(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.connect())
        loop.run_until_complete(self.receive_messages())

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")

        # Start the message processing task
        asyncio.ensure_future(self.process_messages())

    async def send_message(self, message):
        await self.task_queue.put(("send", message))

    async def receive_messages(self):
        while True:
            response = await self.websocket.recv()
            print(f"Received: {response}")
            if self.message_callback:
                self.message_callback(response)

    async def close(self):
        await self.task_queue.put(("close", None))

    async def process_messages(self):
        try:
            while True:
                task, data = await self.task_queue.get()

                if task == "send":
                    await self.websocket.send(data)
                    print(f"Sent: {data}")
                elif task == "close":
                    await self.websocket.close()
                    print("Connection closed")
                    break
        except Exception as e:
            print(f"Error processing messages: {e}")
