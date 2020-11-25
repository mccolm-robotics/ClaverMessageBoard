from .SystemMessages import SystemMessages


class Router:
    def __init__(self, message_queue, notification_manager, mode_objects):
        self.queue = message_queue
        self.__notification_manager = notification_manager
        self.__mode_objects = mode_objects
        self.__system_messages = SystemMessages()
        self.transactions_list = []

    def register_route(self, callback):
        # Route: a communication pathway linking an id (list index) to a function reference
        """ Adds a route (implementation of transaction) callback reference to the list of registered transactions """
        route_id = len(self.transactions_list)
        self.transactions_list.append(callback)
        return route_id

    def process_message(self, message):
        # This assumes that the messages all arrive as single dict with keys "type" and "value"
        print(f"Received Message: {message}")
        if "type" in message:
            if message["type"] == "doodle":
                self.__system_messages.process_message(message)
            # if message["type"] == "games":
            # if message["type"] == "messages":
            # if message["type"] == "photos":
            # if message["type"] == "news":
            # if message["type"] == "timer":
            # if message["type"] == "calendar":
            # if message["type"] == "lists":
            # if message["type"] == "whiteboard":

            # if message["type"] == "notification":
            #     self.__notification_layer.set_notification_message(message["value"])
            # elif message["type"] == "state":
            #     if message["values"] == "users":
            #         self.__notification_layer.set_notification_message(
            #             f"There are now {message['count']} users connected.")
            # elif message["type"] == "request":
            #     if message["value"] == "access_code":
            #         print("Getting access code")
            #         self.messages_sent({"access_code": "4a3b10f"})

    def send_message(self, message):
        """ Sends message to asyncio thread queue for transport by websocket """
        self.queue.put(message)