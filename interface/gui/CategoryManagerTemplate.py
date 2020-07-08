from abc import ABC, abstractmethod


class CategoryManagerTemplate(ABC):

    __UPDATE_FUNCTION = None

    def __init__(self, guiManager):
        """ Constructor """
        super().__init__()
        self.__guiManager = guiManager
        self.__guiManager.registerUpdateCallback(self.updateContentAreaSize)
        self.__contentAreaSize = [1, 1]
        self.__initialized = False


    # Callback
    def updateContentAreaSize(self, contentAreaSize):
        """ Callback function triggered by window resize. Called by GuiManager """
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
        CategoryManagerTemplate.__UPDATE_FUNCTION = func

