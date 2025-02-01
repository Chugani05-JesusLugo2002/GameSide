from datetime import datetime
import re


class Card():
    def __init__(self, card_number: str, exp_date: str, cvc: str):
        self.card_number = card_number
        self.exp_date = exp_date
        self.cvc = cvc

    def validate(self) -> dict|None:
        if (error := self.check_card_number()):
            return error
        if (error := self.check_exp_date()):
            return error
        if (error := self.check_cvc()):
            return error
        return None

    def check_card_number(self) -> dict|None:
        PATTERN = r'^(\d{4}\-){3}\d{4}$'
        if re.match(PATTERN, self.card_number) is None:
            return {'error': 'Invalid card number'}
        return None

    def check_exp_date(self) -> dict|None:
        PATTERN = r'^\d{2}/\d{4}$'
        if re.match(PATTERN, self.exp_date) is None:
            return {'error': 'Invalid expiration date'}
        exp_date = datetime.strptime(self.exp_date, '%m/%Y')
        if exp_date < datetime.now():
            return {'error': 'Card expired'}
        return None

    def check_cvc(self) -> dict|None:
        PATTERN = r'^\d{3}$'
        if re.match(PATTERN, self.cvc) is None:
            return {'error': 'Invalid CVC'}
        return None