import asyncio
import json
import os
import ssl

import pyotp
import websockets

class NodeClient:
    def __init__(self, use_ssl=False):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        if use_ssl:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="server.crt")
            self.ssl_context.load_cert_chain(certfile="client.crt", keyfile="client.key")
        self.uri = "ws://localhost:6789"
        self.main()

    def __getSecretKey(self):
        with open(self.dir_path + "/secret_inSecureStorage.txt", "r") as file:
            for line in file:
                secret_key = line.strip()
        return secret_key

    def __saveSecretKey(self, key):
        with open(self.dir_path + "/secret_inSecureStorage.txt", "w") as file:
            file.write(key)

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
        secret_key = self.__getSecretKey()
        public_key = self.__getPublicKey()
        serial_num = self.__getDeviceID()

        token = pyotp.TOTP(secret_key)
        if self.check_for_public_key():
            credentials = json.dumps({"agent": "node", "nid": serial_num, "token": token.now(), "qdot": public_key, "mode": "WhiteBoard"})
        else:
            credentials = json.dumps({"agent": "node", "nid": serial_num, "mode": "handshake"})

        await websocket.send(credentials)
        response = await websocket.recv()
        data = json.loads(response)
        # Check to see if new public key returned in response
        if "qdot" in data:
            self.__savePublicKey(data["qdot"])
            print(f"Received: {data['qdot']}")
            return True
        return False

    def check_for_public_key(self):
        if self.__getPublicKey():
            return True
        return False

    async def __run(self):
        authenticated = False
        async with websockets.connect(self.uri) as websocket:
            while True:
                try:
                    if not authenticated:
                        if self.check_for_public_key():
                            authenticated = await self.__authenticate_connection(websocket)
                        else:
                            print("Initiating Handshake")
                    else:
                        message = await websocket.recv()
                        print(f"Node: {message}")
                except websockets.ConnectionClosed:
                    break

    def main(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.__run())
        except KeyboardInterrupt:
            pass
        except ConnectionRefusedError:
            print("Connection refused. Server offline")