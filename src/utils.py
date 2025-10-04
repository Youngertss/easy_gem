import random

class InsufficientBalanceException(Exception):
    def __init__(self, user_id: int, required: int, current: int):
        self.user_id = user_id
        self.required = required
        self.current = current


def get_new_bonuse(is_super_bonuse: bool = False):
    values_type = ["money", "multiplier"]
    money_values = [0.1, 0.2, 0.25, 0.5, 0.7, 0.8, 1] #in $
    multiplier_values = [2, 3, 5, 10, 15, 20, 30] #2 means +2%, 30 - +30% etc

    value_type = random.choice(values_type)
    if value_type == "money":
        value = random.choice(money_values)
        if is_super_bonuse:
            value *= 50
    else:
        value = random.choice(multiplier_values)
        if is_super_bonuse:
            value *= 5
    
    return value_type, value