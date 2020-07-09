from abc import ABC, abstractmethod


class SettingsMenuTemplate(ABC):

    __UPDATE_FUNCTION = None

    def __init__(self, settingsManager):
        """ Constructor """
        super().__init__()
        self.__settingsManager = settingsManager
        self.__settingsManager.registerUpdateCallback(self.updateContentAreaSize)
        self.__contentAreaSize = [1, 1]
        self.__initialized = False


    # Callback
    def updateContentAreaSize(self, contentAreaSize):
        """ Called by GuiManager after resize event """
        if self.__initialized:
            if contentAreaSize != self.__contentAreaSize:
                self.__contentAreaSize = contentAreaSize
                if self.__UPDATE_FUNCTION is not None:
                    self.__UPDATE_FUNCTION()
        else:
            self.__initialized = True


    def getContentAreaSize(self):
        """ Access function for content area dimensions """
        return self.__contentAreaSize


    @staticmethod
    def callback_on_resize(func):
        """ Stores a reference to child classes's resize function """
        SettingsMenuTemplate.__UPDATE_FUNCTION = func


