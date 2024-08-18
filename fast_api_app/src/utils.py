import re

class Utils:
    phone_regexp = r'^(8)[0-9]{10}$'
    
    @classmethod
    def check_phone_format(cls, phone_string: str) -> bool:
        print(re.match(cls.phone_regexp, phone_string))
        return bool(re.match(cls.phone_regexp, phone_string))
