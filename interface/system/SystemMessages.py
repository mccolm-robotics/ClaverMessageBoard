class SystemMessages:
    def __init__(self, notification_manager):
        self.__notification_manager = notification_manager
        self.__message_builder = notification_manager.get_message_builder()

    def process_message(self, message):
        # print(f"System message received: {message}")
        if message["property"] == "network":
            if type(message["values"]) is dict:
                if "error" in message["values"]:
                    if message["values"]["error"] == "bad_server_ip":
                        print(self.__message_builder.notification_action(target="settings", action="display_menu", values={'menu': 'network'}))
                        self.__notification_manager.add_notification(mode_action={'target': 'settings', 'action': 'display_menu', 'values': {'menu': 'network'}}, notification="Server IP address unreachable. Review your settings.", priority=2)
                        # pass