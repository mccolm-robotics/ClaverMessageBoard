from abc import ABC, abstractmethod


class Transaction(ABC):
    def __init__(self, router):
        super().__init__()
        self.route_id = router.register_route(self.message_processor)

    def get_route_id(self):
        return self.route_id

    @abstractmethod
    def message_processor(self, message):
        pass