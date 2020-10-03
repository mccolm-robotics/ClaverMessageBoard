import asyncio
import json
import os
import ssl

import pyotp
import websockets
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio

class NodeConnector:
    def __init__(self, claverMessageBoard, use_ssl=False):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        if use_ssl:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="server.crt")
            self.ssl_context.load_cert_chain(certfile="client.crt", keyfile="client.key")
        self.claver_message_board = claverMessageBoard
        self.uri = "ws://localhost:6789"
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def get_loop(self):
        return self.loop

    def __getSecretKey(self):
        with open(self.dir_path + "/secret_inSecureStorage.txt", "r") as file:
            for line in file:
                secret_key = line.strip()
        return secret_key

    def __saveSecretKey(self, key):
        with open(self.dir_path + "/secret_inSecureStorage.txt", "w") as file:
            file.write(key)

    def check_for_public_key(self):
        if self.__getPublicKey():
            return True
        return False

    def __getPublicKey(self):
        with open(self.dir_path + "/public_inSecureStorage.txt", "r") as file:
            for line in file:
                public_key = line.strip()
        return public_key

    def __savePublicKey(self, key):
        with open(self.dir_path + "/public_inSecureStorage.txt", "w") as file:
            file.write(key)

    def __getDeviceID(self):
        # ToDo: Add logic for obtaining device id or serial
        return "000000003d1d1c36"

    async def __authenticate_connection(self, websocket: websockets) -> bool:
        print("Authenticating connection")
        secret_key = self.__getSecretKey()
        public_key = self.__getPublicKey()
        serial_num = self.__getDeviceID()

        token = pyotp.TOTP(secret_key)
        if self.check_for_public_key():
            credentials = json.dumps(
                {"agent": "node", "nid": serial_num, "token": token.now(), "qdot": public_key, "mode": "WhiteBoard"})
        else:
            credentials = json.dumps({"agent": "node", "nid": serial_num, "mode": "handshake"})

        await websocket.send(credentials)
        response = await websocket.recv()
        data = json.loads(response)
        GLib.idle_add(self.claver_message_board.update_gui, data)
        if "qdot" in data:
            self.__savePublicKey(data["qdot"])
            print(f"Received: {data['qdot']}")
            return True
        return False

    async def send_data(self, data):
        message = json.dumps(data)
        await self.websocket.send(message)

    async def __run(self):
        print("In run()")
        authenticated = False
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            while True:
                try:
                    if not authenticated:
                        if self.check_for_public_key():
                            print("found public key")
                            authenticated = await self.__authenticate_connection(websocket)
                        else:
                            print("Initiating Handshake")
                    else:
                        message = await websocket.recv()
                        print(f"Node: {message}")
                        data = json.loads(message)
                        GLib.idle_add(self.claver_message_board.update_gui, data)
                except websockets.ConnectionClosed:
                    break

    def run_asyncio(self):
        try:
            self.loop.run_until_complete(self.__run())
        except KeyboardInterrupt:
            pass
        except ConnectionRefusedError:
            print("Connection refused. Server offline")