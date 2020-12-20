class MessageBuilder:
    """ Abstraction for creating standardized messages that are passed between modules in the Claver client and between
     the Claver client and the Claver server. """

    def notification_action(self, target:str, action:str, values:dict):
        pass