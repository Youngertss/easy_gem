class InsufficientBalanceException(Exception):
    def __init__(self, user_id: int, required: int, current: int):
        self.user_id = user_id
        self.required = required
        self.current = current
