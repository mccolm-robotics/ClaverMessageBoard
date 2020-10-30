import asyncio
import json
import os
import ssl
from pathlib import Path

import pyotp
import websockets
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio
from concurrent.futures import ThreadPoolExecutor

class NodeConnector():
    def __init__(self, claverMessageBoard, queue, use_ssl=False):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.queue = queue
        self.task_queue = None
        self.running = True
        self.access_code = None
        self.config = None
        if use_ssl:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="server.crt")
            self.ssl_context.load_cert_chain(certfile="client.crt", keyfile="client.key")
        self.claver_message_board = claverMessageBoard
        self.uri = "ws://192.168.1.17:6789"
        self.public_key = None
        self.launcher_version = None
        self.launcher_branch = None
        self.application_directory = None
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

    def get_event_loop(self):
        """ Returns the asyncio event loop created for this thread. """
        return self.event_loop

    async def queue_loop(self):
        """ Queue of messages (thread-safe) sent from the GTK event loop. """
        with ThreadPoolExecutor(max_workers=1) as executor:     # Performs asynchronous execution using threads
            while self.running:
                # v must be processed in the same order as they are produced
                data = await self.event_loop.run_in_executor(executor, self.queue.get)
                if data == "cleanup":
                    self.cleanup()
                else:
                    if "access_code" in data:
                        print("New access code sent from GUI.")
                        self.access_code = data["access_code"]
                    if "initialization" in data:
                        self.dir_path = str(Path(self.dir_path).parents[0])     # Hack - Used to store key outside of app dir when run from the launcher
                        self.process_initialization_data(data["initialization"])

    def send_data_to_gui(self, data: dict):
        """ Sends dictionary of directives to GTK for processing. """
        GLib.idle_add(self.claver_message_board.messages_received, data)

    def send_notification_to_gui(self, notification: str) -> None:
        """ Packages a notification string as a directive and sends to GTK for processing. """
        data = {"notification": notification}
        GLib.idle_add(self.claver_message_board.messages_received, data)

    def load_json_from_file(self, settings_file):
        """ Read in the contents of JSON file """
        with open(settings_file) as file:
            return json.load(file)

    def get_rpi_serial(self):
        # Extract serial from cpuinfo file
        cpuserial = ""
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR"
        return cpuserial

    def __getSecretKey(self):
        """ Retrieve secret key from secure storage. """
        if os.path.isfile(self.dir_path + "/secret_inSecureStorage.txt"):
            with open(self.dir_path + "/secret_inSecureStorage.txt", "r") as file:
                for line in file:
                    secret_key = line.strip()
            return secret_key
        else:
            return None

    def __saveSecretKey(self, key):
        """ Save secret key to secure storage. """
        with open(self.dir_path + "/secret_inSecureStorage.txt", "w") as sfile:
            sfile.write(key)

    def check_for_public_key(self):
        """ Checks to see if a public key has been stored for use when authenticating the client connection. """
        if self.public_key is None:
            return self.__getPublicKey()
        else:
            return self.public_key

    def __getPublicKey(self):
        """ Retreives public key from secure storage. """
        if os.path.isfile(self.dir_path + "/public_inSecureStorage.txt"):
            # ToDo: Implement secure storage
            if self.public_key is None:
                with open(self.dir_path + "/public_inSecureStorage.txt", "r") as file:
                    for line in file:
                        self.public_key = line.strip()
            return self.public_key
        else:
            return None

    def __savePublicKey(self, key):
        """ Saves public key in secure storage. """
        # ToDo: Implement secure storage
        with open(self.dir_path + "/public_inSecureStorage.txt", "w") as pfile:
            pfile.write(key)
        self.public_key = key

    def __getDeviceID(self):
        """ Retrieves device serial. """
        serial_num = self.get_rpi_serial()
        if serial_num != "ERROR" and serial_num != "":
            return serial_num
        else:
            return "000000003d1d1c36"

    def process_initialization_data(self, data: dict):
        """ Parses data sent from GTK process during thread creation """
        if type(data) is dict:
            if "launcher_version" in data:
                self.launcher_version = data["launcher_version"]
            if "launcher_branch" in data:
                self.launcher_branch = data["launcher_branch"]
            if "app_dir" in data:
                self.application_directory = data["app_dir"]

    async def __authenticate_connection(self):
        """ Exchanges public data with server to establish trusted connection. """
        if self.application_directory is not None:
            config_file_path = os.getcwd() + "/" + self.application_directory + "/interface/config.txt"
            version_file_path = os.getcwd() + "/" + self.application_directory + "/VERSION.txt"
        else:
            config_file_path = os.getcwd() + "/interface/config.txt"
            version_file_path = os.getcwd() + "/VERSION.txt"
        if os.path.isfile(config_file_path):
            self.config = self.load_json_from_file(config_file_path)
        if os.path.isfile(version_file_path):
            self.config["version"] = self.load_json_from_file(version_file_path)

        secret_key = self.__getSecretKey()
        public_key = self.__getPublicKey()
        serial_num = self.__getDeviceID()
        print(f"File path for key storage: {self.dir_path}")

        token = pyotp.TOTP(secret_key)
        if self.check_for_public_key():
            credentials = json.dumps({
                "agent": "node",
                "nid": serial_num,
                "token": token.now(),
                "qdot": public_key,
                "mode": "WhiteBoard",
                "state": {
                    "launcher_ver": self.launcher_version,
                    "launcher_branch": self.launcher_branch,
                    "board_ver": self.config["version"],
                    "board_branch": self.config["node_branch"]
                }
            })
        else:
            credentials = json.dumps({"agent": "node", "nid": serial_num, "mode": "handshake"})
        await self.websocket.send(credentials)
        try:
            # Server is set to ghost untrusted connections
            response = await asyncio.wait_for(self.websocket.recv(), timeout=10, loop=self.event_loop)
        except:
            return False, "IP address not trusted by server."
        if type(response) == str:
            data = json.loads(response)
            if "request" in data:
                if data["request"] == "access_code":
                    self.send_data_to_gui(data)
                    return False, "access_code"

            if "qdot" in data:
                self.__savePublicKey(data["qdot"])
                return True, None
        return False, "Public key not returned by Server"

    async def send_data(self, data):
        """ Sends message to Claver node client (end point). """
        message = json.dumps(data)
        await self.websocket.send(message)

    async def get_access_code(self):
        """ Sentinel that waits for the GTK process to supply the asyncio thread with an access_code value. """
        while self.running and self.access_code is None:
            await asyncio.sleep(1)

    async def initialize_secure_key_exchange(self):
        """ Constructs chain of trusted key exchange between client and server. Requires the user to register the device
        on the webportal. User submits device_id and ip address to be whitelisted.

        Server -> Client
            1. Secret key is initially created by server. This key is stored on the client during exchange of access code.
            2. Secret key is encrypted on the server with a public key.
            3. Encrypted secret key is stored in db.
            4. Public key is sent to client for storage. Server does not retain copy.
        Client -> Server
            1. Secret key is used to generate a OTP.
            2. OTP and public key sent to server.
            3. Server decrypts secret key stored in DB.
            4. Server confirms OTP using secret key.
            5. Server encrypts secret key with new public key.
            6. New public key sent to the client for storage.
        """
        # Send device id and access code
        serial_num = self.__getDeviceID()
        credentials = json.dumps({"agent": "node", "mode": "handshake", "nid": serial_num, "access_code": self.access_code, "device_name": "Primary", "platform": "RPI 4"})
        print("Sending access code to server.")
        await self.websocket.send(credentials)
        response = await self.websocket.recv()
        data = json.loads(response)
        if "secret_key" in data:
            self.__saveSecretKey(data["secret_key"])
        else:
            print("Server did not send secret key!")
        if "public_key" in data:
            self.__savePublicKey(data["public_key"])
        else:
            print("Server did not send public key!")

    def cleanup(self):
        """ Cancels asyncio tasks and closes the main event loop. Called from the GTK destroy signal by passing a
        cleanup job to the thread queue. """

        print("Cleaning up running tasks and closing event loop.")
        self.running = False
        self.task_queue.cancel()
        self.event_loop.run_until_complete(self.event_loop.shutdown_asyncgens())
        self.event_loop.close()

    def run_asyncio(self):
        """ Starts the websocket client. Initiates the websocket connection with Claver server. """
        try:
            self.task_queue = self.event_loop.create_task(self.queue_loop())
            self.event_loop.run_until_complete(self.__run())  # Specifies the connection coroutine
        except ConnectionRefusedError:
            self.send_notification_to_gui("Server Status: Offline")
            print("Connection refused. Server offline")

    async def __run(self):
        """
        Coroutine: Websocket connection handler. This method receives websocket messages and performs some initial processing on them.
        """
        authenticated = False
        authentication_report = False
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            while self.running:
                try:
                    if not authenticated:
                        if self.check_for_public_key():
                            print("Attempting authentication with stored public key.")
                            result, error = await self.__authenticate_connection()
                            if result:
                                authenticated = True
                            else:
                                print("Public key invalid. Reinitializing chain of trust.")
                                await self.get_access_code()
                                await self.initialize_secure_key_exchange()
                        else:
                            print("No existing public key found. Initializing chain of trust.")
                            await self.__authenticate_connection()
                            await self.get_access_code()
                            await self.initialize_secure_key_exchange()
                    else:
                        if not authentication_report:
                            print("Connection authenticated.")
                            authentication_report = True
                        message = await websocket.recv()
                        self.process_message(message)
                except websockets.ConnectionClosed:
                    break
        print("Connection closed by server.")

    def process_message(self, message):
        print(f"Message from server: {message}")
        data = json.loads(message)
        self.send_data_to_gui(data)

"""
Resources: RPi Serial Number
https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
"""