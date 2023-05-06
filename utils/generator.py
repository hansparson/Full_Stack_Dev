from flask import current_app as app
from datetime import datetime
import pytz
import random


class GeneratorUtils():
    
    def __init__(self):
        self.app = app
    
    def _generate_user_id(self):
        """auto generate id"""
        datetimeNow = datetime.now(pytz.timezone('Asia/Jakarta'))
        datetimeStr = datetimeNow.strftime('%Y%m%d%H%M%S%f')[:-3]
        # format YYYYMMDDHHMMSSFFFXXXXXX
        # F for miliseconds
        return datetimeStr + str(random.randint(100000, 999999))