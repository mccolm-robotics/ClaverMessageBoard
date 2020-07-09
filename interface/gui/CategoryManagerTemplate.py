from abc import ABC, abstractmethod


class CategoryManagerTemplate(ABC):

    __UPDATE_FUNCTION = None

    def __init__(self, guiManager):
        """ Constructor """
        super().__init__()
        self.__guiManager = guiManager
        self.__guiManager.registerUpdateCallback(self.updateContentAreaSize)
        self.__updateCallbacks = []
        self.__contentAreaSize = (1, 1)
        self.__initialized = False


    # Callback
    def updateContentAreaSize(self, contentAreaSize):
        """ Callback function triggered by window resize. Called by GuiManager """
        if self.__initialized:
            # Using tuple: must compare individual elements
            if contentAreaSize[0] != self.__contentAreaSize[0] or contentAreaSize[1] != self.__contentAreaSize[1]:
                self.__contentAreaSize = tuple(contentAreaSize)     # prevent copy by reference
                if self.__UPDATE_FUNCTION is not None:
                    self.__UPDATE_FUNCTION()
        else:
            self.__initialized = True


    def getContentAreaSize(self):
        """ Access function for content area dimensions """
        return self.__contentAreaSize


    # Function decorator. Use with @callback_on_resize
    @staticmethod
    def callback_on_resize(func):
        """ Stores a reference to child classes's resize function """
        CategoryManagerTemplate.__UPDATE_FUNCTION = func

    def updateCallbackFunctions(self, dimensions):
        for function in self.__updateCallbacks:
            function(dimensions)

    def registerUpdateCallback(self, function):
        self.__updateCallbacks.append(function)
