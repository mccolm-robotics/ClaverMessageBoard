
class NotificationManager:
    def __init__(self, notification_layer, alert_layer):
        self.__notification_layer = notification_layer
        self.__alert_layer = alert_layer
        self.__notifications_list = []

    def add_notification(self, message):
        self.__notifications_list.append(message)
        self.__notification_layer.set_notification_message(message["value"])

    def get_notifications_count(self):
        return len(self.__notifications_list)