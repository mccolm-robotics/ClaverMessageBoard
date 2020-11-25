from ..system.Transaction import Transaction


class AuthorizeNode(Transaction):
    def __init__(self, router):
        super().__init__(router)

    def message_processor(self, message):
        print(f"Authorize Node: {message}")