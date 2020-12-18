class SystemMessages:
    def __init__(self, notification_manager):
        self.__notification_manager = notification_manager

    def process_message(self, message):
        # print(f"System message received: {message}")
        if message["property"] == "network":
            if type(message["values"]) is dict:
                if "error" in message["values"]:
                    if message["values"]["error"] == "bad_server_ip":
                        self.__notification_manager.add_notification(mode_action={'mode': 'settings', 'action': 'display_menu', 'value': {'menu': 'network'}}, notification="Server IP address unreachable. Review your settings.", priority=2)
                        # pass